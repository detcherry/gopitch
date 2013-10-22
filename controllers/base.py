import os.path
import logging
import traceback
import sys
import json
import webapp2
import jinja2

from webapp2_extras import sessions
from functools import wraps

from tweepy import auth
from tweepy.api import API

from controllers import config
from models.user import User

def login_required(method):
	@wraps(method)
	def wrapper(self, *args, **kwargs):
		user = self.user
		if not user:
			if self.request.method == "GET":
				# Create a better redirect (TODO) or introduce a popup for login and refresh page after login
				self.redirect("/")
				return
			self.error(403)
		else:
			return method(self, *args, **kwargs)

	return wrapper

class BaseHandler(webapp2.RequestHandler):
	# Custom rendering function
	def render(self, path, values):
		self._values = {}
		if values:
			self._values = values
				
		if self.user and self.user.email is None and self.request.path != "/auth/complete":
			# User has not completed his profile
			self.redirect("/auth/complete")
		
		self._values.update({
			"user": self.user,
			"env": config.ENV,
			"version": config.VERSION,
			"site_url": config.SITE_URL,
			"domain": config.DOMAIN,
			"google_analytics_id": config.GOOGLE_ANALYTICS_ID,
		})
		
		templates = os.path.join(os.path.dirname(__file__),"../templates/")
		jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(templates))
		template = jinja.get_template(path)
		self.response.out.write(template.render(self._values))
	
	def dispatch(self):
		# Get a session store for this request.
		self.session_store = sessions.get_store(request=self.request)
		
		try:
			# Dispatch the request.
			webapp2.RequestHandler.dispatch(self)
		finally:
			# Save all sessions.
			self.session_store.save_sessions(self.response)
	
	@webapp2.cached_property
	def session(self):
		# Returns a session using the default cookie key.
		return self.session_store.get_session()
	
	# Current user stored in session/cookie
	@property
	def user(self):
		if not hasattr(self, "_user"):
			self._user = None;
			user_id = self.session.get("id")
			
			if user_id:
				self._user = User.get_by_id(user_id)
				
		return self._user		
	
	# Handle exceptions, errors that are raised
	def handle_exception(self, exception, debug_mode):
		logging.error(''.join(traceback.format_exception(*sys.exc_info())))
		self.response.out.write(json.dumps({"error":"An error occurred."}))
		
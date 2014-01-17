import os
import logging
import traceback
import sys
import json
import webapp2

from django.template.loader import render_to_string
from django.template.loader import add_to_builtins

from webapp2_extras import sessions
from functools import wraps

from tweepy import auth
from tweepy.api import API

from controllers import config
from models.user import User

def login_required(method):
	@wraps(method)
	def wrapper(self, *args, **kwargs):
		user = self.current_user
		if not user:
			if self.request.method == "GET":
				self.redirect("/auth/signin?next="+self.request.url)
				return
			self.error(403)
		else:
			return method(self, *args, **kwargs)

	return wrapper


def admin_required(method):
	@wraps(method)
	def wrapper(self, *args, **kwargs):
		if not self.admin:
			if self.request.method == "GET":
				self.redirect("/")
				return
			self.error(403)
		else:
			return method(self, *args, **kwargs)

	return wrapper

class BaseHandler(webapp2.RequestHandler):
	# Custom rendering function
	def render(self, path, values):
		os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
		
		self._values = {}
		if values:
			self._values = values
				
		if self.current_user and self.current_user.email is None and self.request.path != "/auth/complete":
			# User has not completed his profile
			self.redirect("/auth/complete")
			
		self._values.update({
			"current_user": self.current_user,
			"admin": self.admin,
			"env": config.ENV,
			"version": config.VERSION,
			"site_url": config.SITE_URL,
			"domain": config.DOMAIN,
			"google_analytics_id": config.GOOGLE_ANALYTICS_ID,
			"cio_site_id": config.CIO_SITE_ID,
			"cio_api_key": config.CIO_API_KEY,
		})
		
		add_to_builtins('ext.templatetags.custom')
		self.response.out.write(render_to_string(path, self._values))
	
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
	def current_user(self):
		if not hasattr(self, "_user"):
			self._current_user = None;
			user_id = self.session.get("id")
			
			if user_id:
				self._current_user = User.get_by_id(user_id)
				
		return self._current_user
	
	@property
	def admin(self):
		if not hasattr(self, "_admin"):
			self._admin = False
			if self.current_user and self.current_user.twitter_id == "79523684":
				self._admin = True
		
		return self._admin
			
	# Handle exceptions, errors that are raised
	def handle_exception(self, exception, debug_mode):
		logging.error(''.join(traceback.format_exception(*sys.exc_info())))
		self.response.out.write(json.dumps({"error":"An error occurred."}))
		
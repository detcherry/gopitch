import os.path
import logging
import traceback
import sys
import json
import webapp2
import jinja2

from webapp2_extras import sessions

from tweepy import auth
from tweepy.api import API

from controllers import config
from models.user import User

class BaseHandler(webapp2.RequestHandler):
	# Custom rendering function
	def render(self, path, values):
		self._values = {}
		if values:
			self._values = values
		
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
		if not hasattr(self, "._user"):
			self._user = None;
			twitter_id = self.session.get("id")
			
			if twitter_id:
				self._user = User.get_by_key_name(twitter_id)
				
		return self._user				
	
	# Handle exceptions, errors that are raised
	def handle_exception(self, exception, debug_mode):
		logging.error(''.join(traceback.format_exception(*sys.exc_info())))
		self.response.out.write(json.dumps({"error":"An error occurred."}))
		
class OauthTwitterSigninHandler(BaseHandler):
	def get(self):
		handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
		
		try:
			authorization_url = handler.get_authorization_url()
		except tweepy.TweepError: 
			print "Error"
		
		# Save the Twitter request key and secret in the session
		self.session["request_token_key"] = handler.request_token.key
		self.session["request_token_secret"] = handler.request_token.secret
		
		self.redirect(authorization_url)
		
class OauthTwitterCallbackHandler(BaseHandler):
	def get(self):
		verifier = self.request.get("oauth_verifier")
		
		# Verfier code there
		if verifier:
			# Get access token
			handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
			handler.set_request_token(self.session.get("request_token_key"), self.session.get("request_token_secret"))
			access_token = handler.get_access_token(verifier)
			
			logging.info("Access token: %s" %(access_token))

			user = User.all().filter("access_token_key", access_token.key).get()
			if user:
				# Update user info if last update > 24 hours
				logging.info("User already exists")				
			else:
				# Save the new user
				logging.info("User did not exist")
				api = API(handler, secure=False)
				temp_user = api.verify_credentials()
				logging.info(temp_user)
				
				user = User(
					key_name = str(temp_user.id),
					username = str(temp_user.screen_name),
					name = str(temp_user.name),
					access_token_key = str(access_token.key),
					access_token_secret = str(access_token.secret),
				)
				user.put()
				logging.info("User @%s saved in datastore"%(user.username))
			
			# Save user in session
			self.session["id"] = str(user.key().name())
			
		self.redirect("/")

class HomeHandler(BaseHandler):
	def get(self):		
		values = {}
		path = "home.html"
		self.render(path, values)



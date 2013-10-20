import logging

from tweepy import auth
from tweepy.api import API

from controllers import config
from controllers.base import BaseHandler

from models.user import User

class AuthSigninHandler(BaseHandler):
	def get(self):
		handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
		
		try:
			authorization_url = handler.get_authorization_url()
		except tweepy.TweepError: 
			logging.error("Could not retrieve Twitter authorization URL")
			print "Error"
		
		# Save the Twitter request key and secret in the session
		self.session["request_token_key"] = handler.request_token.key
		self.session["request_token_secret"] = handler.request_token.secret
		
		self.redirect(authorization_url)
		
class AuthCallbackHandler(BaseHandler):
	def get(self):
		verifier = self.request.get("oauth_verifier")
		
		if verifier:
			# Get access token
			handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
			handler.set_request_token(self.session.get("request_token_key"), self.session.get("request_token_secret"))
			access_token = handler.get_access_token(verifier)
			
			if access_token:
				# Get user			
				logging.info("Access token: %s" %(access_token))
				user = User.all().filter("access_token_key", access_token.key).get()
				if user:
					# Update user info if last update > 24 hours (TODO)
					logging.info("User already exists")				
				else:
					# Save the new user
					logging.info("User did not exist")
					api = API(handler, secure=False)
					temp_user = api.verify_credentials()
					logging.info(temp_user)
					
					# Get the user picture (TODO)
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
				
			else:
				logging.error("No access token from Twitter")
				print "Error"
		else:
			logging.error("No verifier")
			print "Error"
			
		self.redirect("/")

class AuthSignoutHandler(BaseHandler):
	def get(self):
		# Remove all the current user sessions
		self.session.clear()
		
		self.redirect("/")
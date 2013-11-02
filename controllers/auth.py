import logging
import re
import tweepy

from tweepy import auth
from tweepy.api import API

from controllers import config
from controllers.base import BaseHandler

from models.user import User

class AuthSigninHandler(BaseHandler):
	def get(self):
		handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
		
		try:
			authorization_url = handler.get_authorization_url(True)
		except tweepy.TweepError: 
			logging.error("Could not retrieve Twitter authorization URL")
			print "Error"
		
		# Save the Twitter request key and secret in the session
		self.session["request_token_key"] = handler.request_token.key
		self.session["request_token_secret"] = handler.request_token.secret
		self.session["referer"] = self.request.referer
		
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
				user = User.all().filter("twitter_access_token_key", access_token.key).get()
				if user:
					# TODO: Update user info if last update > 24 hours
					logging.info("User already exists")				
				else:
					# Save the new user
					logging.info("User did not exist")
					api = API(handler, secure=False)
					temp_user = api.verify_credentials()
					
					# TODO: Get the Twitter profile picture
					
					user = User(
						twitter_id = str(temp_user.id),
						twitter_access_token_key = str(access_token.key),
						twitter_access_token_secret = str(access_token.secret),
						username = str(temp_user.screen_name),
						name = str(temp_user.name),
					)
					user.put()
					logging.info("User @%s saved in datastore"%(user.username))
		
				# Save user in session
				self.session["id"] = user.key().id()
				
			else:
				logging.error("No access token from Twitter")
				print "Error"
		else:
			logging.error("No verifier")
			print "Error"
		
		# Redirect users to the page they came from
		self.redirect(str(self.session.get("referer")))

class AuthSignoutHandler(BaseHandler):
	def get(self):
		# Remove all the current user sessions
		self.session.clear()
		
		self.redirect("/")
		
class AuthCompleteHandler(BaseHandler):
	def get(self):
		if self.user and self.user.email is None:
			values = {
				"countries": User.get_countries(),
			}
			path = "complete.html"
			self.render(path, values)
		else:
			self.redirect("/")
	
	def post(self):
		user_email = self.request.get("email")
		user_country = self.request.get("country")
		
		user_email_ok = False
		user_country_ok = False
		
		if re.match("[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,4}", user_email):
			user_email_ok = True
			
		countries = User.get_countries()
		for country in countries:
			if user_country == country["code"]:
				user_country_ok = True
				break
			
		if user_email_ok and user_country_ok:			
			user = self.user
			user.email = user_email
			user.country = user_country
			user.put()	
			self.redirect("/")
		else:
			# Display the form again
			values = {}
			path = "complete.html"
			self.render(path, values)
		
		
		
		

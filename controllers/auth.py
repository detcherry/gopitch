import re
import logging
from datetime import datetime
from datetime import timedelta

from tweepy import auth
from tweepy import TweepError
from tweepy.api import API

import cloudstorage as gcs

from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import blobstore
from google.appengine.api import images

from controllers import config
from controllers.base import BaseHandler

from models.user import User

class AuthSigninHandler(BaseHandler):
	def get(self):
		handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
		
		try:
			authorization_url = handler.get_authorization_url(True)
		except TweepError: 
			logging.error("Could not retrieve Twitter authorization URL")
		
		# Save the Twitter request key and secret in the session
		self.session["request_token_key"] = handler.request_token.key
		self.session["request_token_secret"] = handler.request_token.secret
		self.session["next"] = self.request.get("next")
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
				
				if((not user) or (user and user.updated < datetime.now() - timedelta(0,86400))):
					logging.info("Connecting to the Twitter API")
					api = API(handler)
					temp_user = api.verify_credentials()
					temp_image = urlfetch.Fetch(str(temp_user.profile_image_url).replace("_normal", "")).content

					# Transform image into .PNG
					image_manager = images.Image(image_data=temp_image)
					image_manager.rotate(360)
					temp_png = image_manager.execute_transforms()
					logging.info("Encoded into .PNG")

					# Save or update image in Cloud storage
					filename = config.FOLDER + "/" + str(temp_user.id)
					gcs_file = gcs.open(filename,'w',content_type="image/png",options={"x-goog-acl":"public-read"})
					gcs_file.write(temp_png)
					gcs_file.close()
					logging.info("Image saved to Google Cloud Storage")

					# Get avatar
					blob_filename = "/gs" + filename
					blobkey = blobstore.create_gs_key(blob_filename)
					temp_avatar = str(images.get_serving_url(blobkey))
								
					if not user:
						logging.info("User did not exist")

						user = User(
							twitter_id = str(temp_user.id),
							twitter_access_token_key = str(access_token.key),
							twitter_access_token_secret = str(access_token.secret),
							username = str(temp_user.screen_name).lower(),
							name = temp_user.name,
							bio = temp_user.description,
							avatar = temp_avatar,
						)
						
					else:
						logging.info("User had to be updated")

						user.twitter_id = str(temp_user.id)
						user.twitter_access_token_key = str(access_token.key)
						user.twitter_access_token_secret = str(access_token.secret)
						user.username = str(temp_user.screen_name).lower()
						user.name = temp_user.name
						user.bio = temp_user.description
						user.avatar = temp_avatar
											
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
		
		# Redirect users to the page they came from or the page they're supposed to head to
		next = self.session.get("next")
		redirect = self.session.get("referer")
		if next:
			redirect = next
		self.redirect(str(redirect))

class AuthSignoutHandler(BaseHandler):
	def get(self):
		# Remove all the current user sessions
		self.session.clear()
		
		self.redirect("/")
		
class AuthCompleteHandler(BaseHandler):
	def get(self):
		if self.current_user and self.current_user.email is None:
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
		
		user_email_ok = User.validate_email(user_email)
		user_country_ok = User.validate_country(user_country)
			
		if user_email_ok and user_country_ok:			
			user = self.current_user
			user.email = user_email
			user.country = user_country
			user.put()	
			
			# Redirect users to the page they came from or the page they're supposed to head to
			next = self.session.get("next")
			redirect = self.session.get("referer")
			if next:
				redirect = next

			self.redirect(str(redirect))
		else:
			# Display the form again
			values = {
				"countries": User.get_countries(),
			}
			path = "complete.html"
			self.render(path, values)
		
		
		
		

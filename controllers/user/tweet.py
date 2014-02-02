import logging

from tweepy import auth
from tweepy import TweepError
from tweepy.api import API

from controllers import config
from controllers.base import BaseHandler
from controllers.base import login_required

class UserTweetHandler(BaseHandler):
	@login_required
	def post(self):
		tweet = self.request.get("tweet")
		
		if not tweet:
			self.redirect("/")
		else:
			handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
			handler.set_access_token(self.current_user.twitter_access_token_key, self.current_user.twitter_access_token_secret)
			api = API(handler)
			
			try:
				api.update_status(tweet)
				response = "Tweet successfully sent"
			except TweepError:
				logging.error("Could not send tweet.")
				response = "Could not send your tweet. Please try again later."
			
			values = {
				"response": response,
				"next":{
					"content": "Back to homepage",
					"url": "/",
				}
			}
			path = "feedback.html"
			self.render(path, values)				
			
		
		
		
		


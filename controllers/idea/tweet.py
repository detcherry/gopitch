import logging

from tweepy import auth
from tweepy.api import API

from controllers import config
from controllers.base import BaseHandler
from controllers.base import login_required

class IdeaTweetHandler(BaseHandler):
	@login_required
	def post(self):
		tweet = self.request.get("tweet")
		
		if not tweet:
			self.redirect("/")
		else:
			handler = auth.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
			handler.set_access_token(self.current_user.twitter_access_token_key, self.current_user.twitter_access_token_secret)
			api = API(handler, secure=False)
			
			try:
				api.update_status(tweet)
				response = "Idea successfully tweeted."
			except tweepy.TweepError:
				logging.error("Could not send tweet.")
				response = "Could not send your tweet. Please try again later."
			
			values = {
				"response": response
			}
			path = "feedback.html"
			self.render(path, values)				
			
		
		
		
		


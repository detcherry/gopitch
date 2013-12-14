import logging

from controllers import config
from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea
from models.tweet import generate_tweet

class IdeaPitchHandler(BaseHandler):
	@login_required
	def get(self):	
		values = {
			"status": "new",
			"url": "/idea/pitch",
			"steps": Idea.get_current_steps(),
		}
		path = "idea/pitch.html"
		self.render(path, values)
	
	@login_required
	def post(self):
		validated, title, answers = Idea.validate(self.request)
		
		if not validated:
			self.redirect("/idea/pitch")
		else:
			# Record the idea and redirect to homepage
			idea = Idea(
				title = title,
				author = self.current_user.key(),
				answers = answers,
				version = Idea.get_current_version(),
				country = self.current_user.country,
			)
			idea.put()
			
			user = self.current_user
			user.ideas += 1
			user.put()
			
			text = "I just pitched a new startup idea on @getpitchd: " + idea.title
			url = config.SITE_URL + "/idea/" + str(idea.key().id())
			tweet = generate_tweet(text, url)
			
			response = "Congratulations for pitching your idea on getpitchd!"
			next = "Now, tweet your friends about it!"
			
			values = {
				"response": response,
				"next": next,
				"tweet": tweet,
			}
			path = "idea/tweet.html"
			self.render(path, values)
			
		
		

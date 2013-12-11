import logging

from controllers import config
from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea
from models.tweet import generate_tweet

class IdeaPitchHandler(BaseHandler):

	def __init__(self, request, response):
		super(IdeaPitchHandler, self).__init__(request, response)
		
		self.current_version = "0"
		self.steps = Idea.get_steps(self.current_version)

	@login_required
	def get(self):	
		values = {
			"steps": self.steps,
		}
		path = "idea/pitch.html"
		self.render(path, values)
	
	@login_required
	def post(self):
		incorrect = False
		answers = []
		title = self.request.get("title")
				
		if title == "":
			incorrect = True
		else:	
			logging.info("Title: %s" % (title)) 
			for step in self.steps:
				attribute = "answer_" + step["slug"]
				answer = self.request.get(attribute)

				if answer and len(answer) <= 140:
					answers.append(answer)
				else:
					incorrect = True
					break
		
		if incorrect:
			self.redirect("/idea/pitch")
		else:
			# Record the idea and redirect to homepage
			idea = Idea(
				title = title,
				author = self.current_user.key(),
				answers = answers,
				version = self.current_version,
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
			
		
		

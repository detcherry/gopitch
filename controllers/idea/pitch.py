import logging

from controllers import config
from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea

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
			
			short_url_length = 22 # See https://dev.twitter.com/docs/api/1.1/get/help/configuration
			tweet = "I just pitched a new startup idea on @getpitchd: "
			
			characters_left = 140 - len(tweet) - len(" ") - short_url_length
			if len(idea.title) < characters_left:
				tweet += idea.title + " "
			else:
				tweet += idea.title[characters_left-3] + "..." + " "
			
			tweet += config.SITE_URL + "/idea/" + str(idea.key().id())
			values = {
				"tweet": tweet,
			}
			path = "idea/tweet.html"
			self.render(path, values)
			
		
		

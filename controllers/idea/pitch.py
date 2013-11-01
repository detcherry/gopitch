import logging

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
		path = "pitch.html"
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
				author = self.user.key(),
				answers = answers,
				version = self.current_version,
			)
			idea.put()
			
			self.redirect("/")
		
		
		

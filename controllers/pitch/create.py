import logging

from controllers.base import BaseHandler
from controllers.base import login_required

from models.pitch import Pitch

class PitchCreateHandler(BaseHandler):

	def __init__(self, request, response):
		super(PitchCreateHandler, self).__init__(request, response)
		
		self.version = "0"
		
		# Steps
		self.steps = [
			"Problem",
			"Solution",
			"Opportunity",
			"Competitors",
			"Business Model",
			"Acquisition",
			"Milestones"
		]
		
		# Questions
		self.questions = [
			"What is the problem you're trying to solve? Who has this problem?",
			"What are you going to build?",
			"What's new about what you're building? What are people forced to do because you don't exist?",
			"Who are your competitors?",
			"How are you going to make money?",
			"How will potential users know about you?",
			"Are you posting this idea for fun or would you like to dig into it? Find a cofounder?"
		]

	@login_required
	def get(self):	
		values = {
			"steps": self.steps,
			"questions": self.questions,
		}
		path = "pitch.html"
		self.render(path, values)
	
	@login_required
	def post(self):
		title = self.request.get("title")
		
		answer_0 = self.request.get("answer_0")
		answer_1 = self.request.get("answer_1")
		answer_2 = self.request.get("answer_2")
		answer_3 = self.request.get("answer_3")
		answer_4 = self.request.get("answer_4")
		answer_5 = self.request.get("answer_5")
		answer_6 = self.request.get("answer_6")
		
		if title and answer_0 and answer_1 and answer_2 and answer_3 and answer_4 and answer_5 and answer_6:
			self.answers = [answer_0, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6]
			
			# Record the pitch and redirect to homepage
			pitch = Pitch(
				title = title,
				author = self.user.key(),
				answers = self.answers,
				version = self.version,
			)
			pitch.put()
			self.redirect("/")
		else:
			self.redirect("/pitch/create")
		

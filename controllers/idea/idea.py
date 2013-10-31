import logging

from controllers.base import BaseHandler

from models.idea import Idea

class IdeaHandler(BaseHandler):
	def get(self, id):
		idea = Idea.get_by_id(int(id))
		extended_steps = Idea.get_extended_steps(idea)
		
		values = {
			"title": idea.title,
			"extended_steps": extended_steps,
		}
		path = "idea.html"
		self.render(path, values)
		
		
		
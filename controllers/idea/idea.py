import logging

from controllers.base import BaseHandler

from models.idea import Idea
from models.user import User

class IdeaHandler(BaseHandler):
	def get(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			extended_steps = Idea.get_extended_steps(idea)
		
			author_key = Idea.author.get_value_for_datastore(idea)
			author = User.get(author_key)
		
			values = {
				"id": idea.key().id(),
				"title": idea.title,
				"author": author,
				"extended_steps": extended_steps,
			}
			path = "idea/idea.html"
			self.render(path, values)
		else:
			logging.error("Idea does not exist")
			self.response.out.write("Idea does not exist")
			

		
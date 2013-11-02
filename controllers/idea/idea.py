import logging

from error import GetpitchdError

from controllers.base import BaseHandler

from models.idea import Idea
from models.user import User

class IdeaHandler(BaseHandler):
	def get(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			extended_idea = Idea.get_extended_idea(idea)
		
			author_key = Idea.author.get_value_for_datastore(idea)
			author = User.get(author_key)

			values = {
				"extended_idea": extended_idea,
				"author": author,
			}
			path = "idea/idea.html"
			self.render(path, values)
		else:
			raise GetpitchdError("Idea does not exist")
			

		
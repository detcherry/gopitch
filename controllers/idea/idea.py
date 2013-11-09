import logging

from error import GetpitchdError

from controllers.base import BaseHandler

from models.idea import Idea
from models.user import User
from models.feedback import Feedback

class IdeaHandler(BaseHandler):
	def get(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			extended_idea = Idea.get_extended_idea(idea)
		
			author_key = Idea.author.get_value_for_datastore(idea)
			author = User.get(author_key)
			
			if(self.current_user):
				feedback = Feedback.all().filter("author =", self.current_user.key()).filter("idea =", idea.key()).get()
			
			values = {
				"extended_idea": extended_idea,
				"author": author,
				"feedback": feedback,
			}
			path = "idea/idea.html"
			self.render(path, values)
		else:
			raise GetpitchdError("Idea does not exist")
			

		
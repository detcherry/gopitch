import logging

from error import GetpitchdError

from controllers.base import BaseHandler
from controllers.base import login_required

from models.feedback import Feedback
from models.idea import Idea

class FeedbackDeleteHandler(BaseHandler):	
	@login_required
	def post(self, key_name):
		feedback = Feedback.get_by_key_name(key_name)
		
		if(feedback):
			author_key = Feedback.author.get_value_for_datastore(feedback)

			if(author_key == self.current_user.key()):
				
				idea_key = Feedback.idea.get_value_for_datastore(feedback)
				idea = Idea.get(idea_key)
				
				if(feedback.content == "positive"):
					idea.positive += -1
				else:
					idea.negative += -1
				
				idea.put()
				feedback.delete()
						
				values = {
					"response": "Feedback deleted."
				}
				path = "feedback.html"		
				self.render(path, values)
			else:
				raise GetpitchdError("Not authorized to delete idea")
		else:
			raise GetpitchdError("Idea does not exist")
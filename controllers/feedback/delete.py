import logging

from error import GetpitchdError

from controllers.base import BaseHandler
from controllers.base import login_required

from models.feedback import Feedback

class FeedbackDeleteHandler(BaseHandler):	
	@login_required
	def post(self, key_name):
		feedback = Feedback.get_by_key_name(key_name)
		
		if(feedback):
			author_key = Feedback.author.get_value_for_datastore(feedback)

			if(author_key == self.current_user.key()):
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
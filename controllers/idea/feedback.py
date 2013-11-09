import logging

from error import GetpitchdError

from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea
from models.user import User
from models.feedback import Feedback

class IdeaFeedbackHandler(BaseHandler):
	@login_required
	def post(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			content = self.request.get("feedback")
			
			if(content=="positive" or content=="negative"):
				feedback = Feedback(
					key_name = str(self.current_user.key().id()) + "_" + str(idea.key().id()),
					author = self.current_user.key(),
					idea = idea.key(),
					content = content,
				)
				feedback.put()
				
				if(content == "positive"):
					idea.positive += 1
				else:
					idea.negative += 1
				idea.put()
				
				extended_idea = Idea.get_extended_idea(idea)
				
				author_key = Idea.author.get_value_for_datastore(idea)
				author = User.get(author_key)
				
				values = {
					"feedback": feedback,
					"extended_idea": extended_idea,
					"author": author,
				}
				path = "idea/feedback.html"
				self.render(path, values)
			else:
				raise GetpitchdError("Forbidden content")
		else:
			raise GetpitchdError("Idea does not exist")
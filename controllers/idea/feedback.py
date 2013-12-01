import logging

from error import GetpitchdError

from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea
from models.user import User
from models.feedback import Feedback
from models.comment import Comment

class IdeaFeedbackHandler(BaseHandler):
	@login_required
	def post(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			content = self.request.get("feedback")
			
			if(content=="positive" or content=="negative"):
				key_name = str(self.current_user.key().id()) + "_" + str(idea.key().id())
				existing_feedback = Feedback.get_by_key_name(key_name)
				
				if not existing_feedback:	
					feedback = Feedback(
						key_name = key_name,
						author = self.current_user.key(),
						idea = idea.key(),
						content = content,
					)
					feedback.put()
								
					if(content == "positive"):
						idea.positive += 1
					else:
						idea.negative += 1
				
					text = self.request.get("text")
					if text:
						comment = Comment(
							idea = idea.key(),
							author = self.current_user.key(),
							text = text,
						)

						comment.put()
						idea.comments += 1
				
					idea.put()
								
					values = {
						"response": "Thanks for giving your feedback!"
					}
					path = "feedback.html"
					self.render(path, values)
				else:
					raise GetpitchdError("Feedback already sent")
			else:
				raise GetpitchdError("Forbidden feedback")
		else:
			raise GetpitchdError("Idea does not exist")
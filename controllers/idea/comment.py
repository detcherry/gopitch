import logging

from google.appengine.ext import db

from error import GetpitchdError
from controllers.base import BaseHandler
from controllers.base import login_required
from models.idea import Idea
from models.comment import Comment

class IdeaCommentHandler(BaseHandler):
	@login_required
	def post(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			text = self.request.get("text")
			
			if(text is not ""):
				comment = Comment(
					idea = idea.key(),
					author = self.current_user.key(),
					text = text[:139],
				)
				
				comment.put()
				idea.comments += 1
				idea.put()

				values = {
					"response": "Comment posted."
				}
				path = "feedback.html"
				self.render(path, values)
				
			else:
				raise GetpitchdError("Comment text is empty")

		else:
			raise GetpitchdError("Idea does not exist")		
		

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
			reply_to_id = self.request.get("reply_to")
			
			comment = Comment(
				author = self.current_user.key(),
				text = self.request.get("text")[:139]
			)
			
			if(reply_to_id is not ""):
				reply_to_comment = Comment.get_by_id(int(reply_to_id))

				if(reply_to_comment):
					comment.reply_to = reply_to_comment.key()
					comment.depth = reply_to_comment.depth + 1
				else:
					raise GetpitchdError("Comment in reply to does not exist")
			
			comment.put()
			
			idea.comments += 1
			idea.put()
			
			values = {
				"response": "Comment posted."
			}
			path = "feedback.html"
			self.render(path, values)
			
		else:
			raise GetpitchdError("Idea does not exist")		
		

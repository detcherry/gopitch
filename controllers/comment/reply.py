import logging

from error import GetpitchdError

from controllers.base import BaseHandler
from controllers.base import login_required

from models.comment import Comment
from models.user import User
from models.idea import Idea

class CommentReplyHandler(BaseHandler):
	@login_required
	def get(self, id):
		comment = Comment.get_by_id(int(id))
		
		if(comment):
			author_key = Comment.author.get_value_for_datastore(comment)
			author = User.get(author_key)
			
			values = {
				"comment": comment,
				"author": author,
			}
			path = "comment/reply.html"
			self.render(path, values)
			
		else:
			raise GetpitchdError("Comment does not exist.")
	
	@login_required
	def post(self, id):
		comment = Comment.get_by_id(int(id))
		
		if(comment):
			text = self.request.get("text")
			
			if(text is not ""):
				idea_key = Comment.idea.get_value_for_datastore(comment)
				idea = Idea.get(idea_key)
				
				reply = Comment(
					idea = idea_key,
					author = self.current_user.key(),
					reply_to = comment.key(),
					text = text,
				)
				
				reply.put()
				idea.comments += 1
				idea.put()
				
				values = {
					"response" : "Replied sent",
					"next":{
						"content": "Back",
						"url": "/idea/"+str(idea.key().id())
					}
				}
				path = "feedback.html"
				self.render(path, values)
				
			else:
				raise GetpitchdError("Comment text is empty")
			
		else:
			raise GetpitchdError("Comment does not exist.")
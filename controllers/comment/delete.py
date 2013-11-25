import logging

from error import GetpitchdError

from controllers.base import BaseHandler
from controllers.base import login_required

from models.comment import Comment
from models.idea import Idea

class CommentDeleteHandler(BaseHandler):
	@login_required
	def get(self, id):
		comment = Comment.get_by_id(int(id))
		
		if(comment):
			author_key = Comment.author.get_value_for_datastore(comment)
		
			if(author_key == self.current_user.key()):
				
				idea_key = Comment.idea.get_value_for_datastore(comment)
				idea = Idea.get(idea_key)
				
				values = {
					"comment": comment,
					"idea": idea,
				}
				path = "comment/delete.html"
				self.render(path, values)
				
			else:
				raise GetpitchdError("Not authorized to delete comment.")
		
		else:
			raise GetpitchdError("Comment does not exist.")
	
	@login_required
	def post(self, id):
		comment = Comment.get_by_id(int(id))
		
		if(comment):
			author_key = Comment.author.get_value_for_datastore(comment)
			
			if(author_key == self.current_user.key()):

				idea_key = Comment.idea.get_value_for_datastore(comment)
				idea = Idea.get(idea_key)
				
				idea.comments -= 1
				idea.put()
				comment.delete() 
				
				# Note: children comments of a deleted comment won't be displayed but they still remain in the comments counter.
								
				values = {
					"response": "Comment deleted."
				}
				path = "feedback.html"		
				self.render(path, values)
				
			else:
				raise GetpitchdError("Not authorized to delete comment.")
			
		else:
			raise GetpitchdError("Comment does not exist.")
		

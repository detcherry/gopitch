import logging
import json

from google.appengine.ext import db

from error import GetpitchdError
from controllers.base import BaseHandler
from controllers.base import login_required
from models.idea import Idea
from models.comment import Comment
from models.event import IdeaCommentEvent

class IdeaCommentHandler(BaseHandler):
	@login_required
	def post(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
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
				
				event = IdeaCommentEvent(self.current_user, comment, idea)

				values = {
					"response": "Comment posted",
					"next":{
						"content": "Back",
						"url": "/idea/"+str(idea.key().id()),
					}
				}
				path = "feedback.html"
				self.render(path, values)
			else:
				raise GetpitchdError("Comment text is empty")

		else:
			raise GetpitchdError("Idea does not exist")		
		

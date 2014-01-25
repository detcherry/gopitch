import logging

from controllers.base import BaseHandler
from controllers.base import login_required

class UserSettingsHandler(BaseHandler):
	@login_required
	def get(self):
		values = {}
		path = "settings.html"
		self.render(path, values)				
	
	@login_required
	def post(self):
		email_idea_comment = False
		email_idea_feedback = False
		email_comment_reply = False
		
		if self.request.get("idea-comment"):
			email_idea_comment = True
		if self.request.get("idea-feedback"):			
			email_idea_feedback = True
		if self.request.get("comment-reply"):			
			email_comment_reply = True
				
		user = self.current_user
		user.email_idea_comment = email_idea_comment
		user.email_idea_feedback = email_idea_feedback
		user.email_comment_reply = email_comment_reply
		user.put()
		
		values = {
			"response": "Settings updated",
			"next":{
				"content": "Back to my profile",
				"url": "/"+user.username,
			}
		}
		path = "feedback.html"
		self.render(path, values)
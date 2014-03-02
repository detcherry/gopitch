import logging

from controllers.base import BaseHandler
from controllers.base import login_required

from models.user import User

class UserSettingsHandler(BaseHandler):
	@login_required
	def get(self):
		countries = User.get_countries()
		for c in countries:
			c["selected"] = False
			if c["code"] == self.current_user.country:
				c["selected"] = True

		values = {
			"countries": countries
		}
		path = "settings.html"
		self.render(path, values)				
	
	@login_required
	def post(self):
		user_email = self.request.get("email")
		user_country = self.request.get("country")

		user = self.current_user

		if User.validate_email(user_email):
			user.email = user_email

		if User.validate_country(user_country):
			user.country = user_country

		email_idea_comment = False
		email_idea_feedback = False
		email_comment_reply = False
		
		if self.request.get("idea-comment"):
			email_idea_comment = True
		if self.request.get("idea-feedback"):			
			email_idea_feedback = True
		if self.request.get("comment-reply"):			
			email_comment_reply = True
				
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
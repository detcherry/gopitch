import logging

from datetime import datetime
from calendar import timegm

from error import GetpitchdError

from controllers.base import BaseHandler

from models.idea import Idea
from models.user import User

class UserHandler(BaseHandler):
	def get(self, username):
		user = User.all().filter("username =", str(username).lower()).get()
		
		if user:
			ideas, offset = Idea.get_last_ideas(user=user, offset=self.request.get("offset"))

			authors = []
			for idea in ideas:
				authors.append(user)

			values = {
				"feed": zip(ideas, authors),
				"user": user,
			}

			if offset:
				values["more_ideas_url"] = "/"+user.username+"?offset="+str(offset)
			
			path = "user.html"
			self.render(path, values)
		else:
			raise GetPitchdError("User does not exist")
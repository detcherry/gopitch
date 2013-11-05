import logging

from error import GetpitchdError

from controllers.base import BaseHandler

from models.idea import Idea
from models.user import User

class UserHandler(BaseHandler):
	def get(self, username):
		user = User.all().filter("username =", str(username).lower()).get()
		ideas = Idea.all().filter("author =", user.key()).order("-created").fetch(50)
		values = {
			"user": user,
			"ideas": ideas,
		}
		path = "user.html"
		self.render(path, values)
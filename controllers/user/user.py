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
			values = {}

			if self.request.get("offset"):
				offset = datetime.utcfromtimestamp(int(self.request.get("offset")))
			else:
				offset = datetime.utcnow()

			size = 50;
			q = Idea.all()
			q.filter("author = ", user.key())
			q.filter("created <", offset)
			q.order("-created")
			ideas = q.fetch(size+1)

			new_offset = None
			if(len(ideas)==size+1):
				last_idea = ideas[len(ideas)-2]
				new_offset = timegm(last_idea.created.utctimetuple())
				values["offset"]=new_offset
				del ideas[-1]

			values.update({
				"user": user,
				"ideas": ideas,
			})

			path = "user.html"
			self.render(path, values)
		else:
			raise GetPitchdError("User does not exist")
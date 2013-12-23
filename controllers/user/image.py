import logging

from error import GetpitchdError

from google.appengine.api.images import Image

from controllers.base import BaseHandler

from models.user import User

class UserImageHandler(BaseHandler):
	def get(self, username):
		user = User.all().filter("username =", str(username).lower()).get()
		
		if user:
			self.response.headers['Content-Type'] = 'image'
			self.response.out.write(user.image)
		else:
			raise GetPitchdError("User does not exist")		
import logging

from google.appengine.ext import db

from controllers.base import BaseHandler

class HomeHandler(BaseHandler):
	def get(self):
		values = {}

		if self.current_user and self.current_user.country:
			country_url = "/c/"+self.current_user.country.lower()
			self.redirect(country_url)
		else:
			path = "welcome.html"
			self.render(path, values)
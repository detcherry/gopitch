import logging

from datetime import datetime
from calendar import timegm

from google.appengine.ext import db

from controllers.base import BaseHandler

from models.idea import Idea

class HomeHandler(BaseHandler):
	def get(self):
		values = {}

		ideas, offset = Idea.get_last_ideas(offset=self.request.get("offset"))

		author_keys = []
		for idea in ideas:
			author_keys.append(Idea.author.get_value_for_datastore(idea))
		authors = db.get(author_keys)

		values["feed"] = zip(ideas, authors)
		
		if offset:
			values["more_ideas_url"] = "/?offset="+str(offset)

		path = "home.html"

		self.render(path, values)
import logging

from datetime import datetime
from calendar import timegm

from error import GetpitchdError

from google.appengine.ext import db

from controllers.base import BaseHandler

from models.user import User
from models.idea import Idea

class CountryHandler(BaseHandler):
	def get(self, country):
		values = {}

		country_name = User.get_country_name(country)

		if country_name:
			values["country_name"] = country_name.lower().capitalize()
			ideas, offset = Idea.get_last_ideas(country=country,offset=self.request.get("offset"))

			author_keys = []
			for idea in ideas:
				author_keys.append(Idea.author.get_value_for_datastore(idea))
			authors = db.get(author_keys)

			values["feed"] = zip(ideas, authors)
			
			if offset:
				values["more_ideas_url"] = "/?offset="+str(offset)

			path = "country.html"

			self.render(path, values)
		else:
			raise GetpitchdError("Country does not exist")
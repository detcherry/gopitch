import logging

from error import GetpitchdError

from google.appengine.ext import db

from controllers.base import BaseHandler

from models.user import User
from models.idea import Idea

class IdeasHandler(BaseHandler):
	def get(self, selector):
		values = {}

		offset = self.request.get("offset")
		new_offset = None

		if selector == "all":
			ideas, new_offset = Idea.get_last_ideas(offset=offset)
		else:

			country_name = User.get_country_name(selector)

			if country_name:
				country = selector
				values["country_name"] = country_name.lower().capitalize()
				values["country_code"] = country.lower()

				ideas, new_offset = Idea.get_last_ideas(country=country,offset=offset)

			else:
				raise GetpitchdError("Country does not exist")

		author_keys = []
		for idea in ideas:
			author_keys.append(Idea.author.get_value_for_datastore(idea))
		authors = db.get(author_keys)

		values["feed"] = zip(ideas, authors)
		
		if new_offset:
			values["more_ideas_url"] = self.request.path + "?offset="+str(new_offset)

		path = "ideas.html"
		self.render(path, values)
import logging

from datetime import datetime
from calendar import timegm

from google.appengine.ext import db

from controllers.base import BaseHandler

from models.idea import Idea

class HomeHandler(BaseHandler):
	def get(self):
		values = {}

		if self.request.get("offset"):
			offset = datetime.utcfromtimestamp(int(self.request.get("offset")))
		else:
			offset = datetime.utcnow()

		size = 50;
		q = Idea.all()
		#q.filter("country = ", self.current_user.country)
		q.filter("created <", offset)
		q.order("-created")
		ideas = q.fetch(size+1)

		new_offset = None
		if(len(ideas)==size+1):
			last_idea = ideas[len(ideas)-2]
			new_offset = timegm(last_idea.created.utctimetuple())
			values["offset"]=new_offset
			del ideas[-1]

		author_keys = []
		for idea in ideas:
			author_keys.append(Idea.author.get_value_for_datastore(idea))
		authors = db.get(author_keys)

		values["feed"] = zip(ideas, authors)
		path = "home.html"

		self.render(path, values)
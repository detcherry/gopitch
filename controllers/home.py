from google.appengine.ext import db

from controllers.base import BaseHandler

from models.idea import Idea

class HomeHandler(BaseHandler):
	def get(self):
		ideas = Idea.all().order("-created").fetch(50)
		author_keys = []
		for idea in ideas:
			author_keys.append(Idea.author.get_value_for_datastore(idea))
		authors = db.get(author_keys)
		
		values = {
			"feed": zip(ideas, authors),
		}
		path = "home.html"
		self.render(path, values)
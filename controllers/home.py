from controllers.base import BaseHandler

from models.idea import Idea

class HomeHandler(BaseHandler):
	def get(self):
		ideas = Idea.all().order("-created").fetch(50)
		# TODO: pagination for ideaes
		
		values = {
			"ideas" : ideas,
		}
		path = "home.html"
		self.render(path, values)
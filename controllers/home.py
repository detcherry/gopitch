from controllers.base import BaseHandler

from models.pitch import Pitch

class HomeHandler(BaseHandler):
	def get(self):
		pitches = Pitch.all().order("-created").fetch(30)
		values = {
			"pitches" : pitches,
		}
		path = "home.html"
		self.render(path, values)
from controllers.base import BaseHandler
from controllers.base import login_required

class PitchCreateHandler(BaseHandler):
	@login_required
	def get(self):	
		values = {}
		path = "pitch.html"
		self.render(path, values)
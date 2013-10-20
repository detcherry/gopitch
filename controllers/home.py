from controllers.base import BaseHandler

class HomeHandler(BaseHandler):
	def get(self):		
		values = {}
		path = "home.html"
		self.render(path, values)
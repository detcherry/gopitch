import logging

from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea

class IdeaDeleteHandler(BaseHandler):
	@login_required
	def get(self, id):	
		values = {
			"id" : id,
		}
		path = "idea/delete.html"
		self.render(path, values)
	
	
	@login_required
	def post(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			author_key = Idea.author.get_value_for_datastore(idea)

			if(author_key == self.user.key() or self.admin):
				idea.delete()
		
				values = {
					"response": "Idea deleted"
				}
				path = "idea/deleted.html"		
				self.render(path, values)
			else:
				logging.error("Not authorized to delete idea")
				self.response.out.write("Not authorized to delete idea")
		else:
			logging.error("Idea does not exist")
			self.response.out.write("Idea does not exist")
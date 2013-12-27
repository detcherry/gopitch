import logging

from error import GetpitchdError

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

			if(author_key == self.current_user.key() or self.admin):
				idea.delete()
				
				user = self.current_user
				user.ideas -= 1
				user.put()
		
				values = {
					"response": "Your idea has been deleted.",
					"next": {
						"content": "Back to homepage",
						"url":"/",
					}
				}
				path = "feedback.html"		
				self.render(path, values)
			else:
				raise GetpitchdError("Not authorized to delete idea")
		else:
			raise GetpitchdError("Idea does not exist")
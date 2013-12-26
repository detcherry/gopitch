import logging

from error import GetpitchdError

from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea

class IdeaEditHandler(BaseHandler):
	@login_required
	def get(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			author_key = Idea.author.get_value_for_datastore(idea)
			
			if(author_key == self.current_user.key() or self.admin):
				extended_idea = Idea.get_extended_idea(idea)
								
				values = {
					"status": "edit",
					"title": extended_idea["title"],
					"id": extended_idea["id"],
					"url": "/idea/" + str(extended_idea["id"]) + "/edit",
					"steps": extended_idea["extended_steps"],
				}
				path = "idea/pitch.html"
				self.render(path, values)		
			
			else:
				raise GetpitchdError("Not authorized to edit idea")
		
		else:
			raise GetpitchdError("Idea does not exist")
		
		
	@login_required
	def post(self, id):
		idea = Idea.get_by_id(int(id))	
		
		if(idea):
			author_key = Idea.author.get_value_for_datastore(idea)
			
			if(author_key == self.current_user.key() or self.admin):
				validated, title, answers = Idea.validate(self.request, idea)
		
				if not validated:
					self.redirect("/idea/"+str(idea.key().id())+"/edit")
				else:
					idea.title = title
					idea.answers = answers
					idea.put()
			
					values = {
						"response": "Idea updated"
					}
					path = "feedback.html"		
					self.render(path, values)
					
			else:
				raise GetpitchdError("Not authorized to edit idea")

		else:
			raise GetpitchdError("Idea does not exist")
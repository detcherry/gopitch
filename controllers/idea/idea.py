import logging

from error import GetpitchdError

from controllers.base import BaseHandler

from models.idea import Idea
from models.user import User
from models.feedback import Feedback
from models.comment import Comment

class IdeaHandler(BaseHandler):
	def get(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			extended_idea = Idea.get_extended_idea(idea)
		
			author = User.get(Idea.author.get_value_for_datastore(idea))
			
			feedback = None
			if(self.current_user):
				feedback = Feedback.all().filter("author =", self.current_user.key()).filter("idea =", idea.key()).get()
			
			# Fetch comments
			comments = Comment.all().filter('idea = ', idea.key()).fetch(1000)
			
			# Filter comments which are not replies to and those from the others
			threaded, children, depths = [], [], []
			for comment in comments:
				if Comment.reply_to.get_value_for_datastore(comment) is None:
					threaded.append(comment)
					depths.append(0)
				else:
					children.append(comment)
			
			# Filter comments which are not replies to by date (desc)
			tosort = [(c.created, c) for c in threaded]
			tosort.sort()
			tosort.reverse()
			threaded = [c for _, c in tosort]
						
			# Filter children by date (asc)
			tosort = [(c.created, c) for c in children]
			tosort.sort()
			children = [c for _, c in tosort]
						
			# Insert children comments at the right place
			for comment in children:
				i = 0
				parents = list(threaded)
				for parent in parents:
					if parent.key() == Comment.reply_to.get_value_for_datastore(comment):
						threaded.insert(1 + i, comment)
						depths.insert(1 + i, depths[i] + 1)
						i = i + 2
					else:
						i = i + 1
			
			# Get authors 
			authors_keys = [Comment.author.get_value_for_datastore(c) for c in threaded]
			authors = User.get(authors_keys)
			
			values = {
				"extended_idea": extended_idea,
				"author": author,
				"feedback": feedback,
				"comments": zip(authors, threaded, depths),
			}
			path = "idea/idea.html"
			self.render(path, values)
		else:
			raise GetpitchdError("Idea does not exist")
			

		
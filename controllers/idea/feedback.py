import logging
import json

from error import GetpitchdError

from google.appengine.api.taskqueue import Task

from controllers import config
from controllers.base import BaseHandler
from controllers.base import login_required

from models.idea import Idea
from models.user import User
from models.feedback import Feedback
from models.comment import Comment
from models.tweet import generate_tweet
from models.event import IdeaFeedbackEvent

class IdeaFeedbackHandler(BaseHandler):
	@login_required
	def post(self, id):
		idea = Idea.get_by_id(int(id))
		
		if(idea):
			content = self.request.get("feedback")
			
			if(content=="positive" or content=="negative"):
				key_name = str(self.current_user.key().id()) + "_" + str(idea.key().id())
				existing_feedback = Feedback.get_by_key_name(key_name)
				
				if not existing_feedback:	
					feedback = Feedback(
						key_name = key_name,
						author = self.current_user.key(),
						idea = idea.key(),
						content = content,
					)
					feedback.put()
								
					if(content == "positive"):
						idea.positive += 1
					else:
						idea.negative += 1
				
					text = self.request.get("text")
					if text:
						comment = Comment(
							idea = idea.key(),
							author = self.current_user.key(),
							text = text,
						)
						comment.put()
						idea.comments += 1
				
					idea.put()
					
					if text:
						event = IdeaFeedbackEvent(self.current_user, feedback, idea, text)
					else:
						event = IdeaFeedbackEvent(self.current_user, feedback, idea)
					
					if(content == "positive"):
						author_key = Idea.author.get_value_for_datastore(idea)
						author = User.get(author_key)
						
						text = "I'm enthusiastic about a new startup idea pitched by @" + author.username + " on @gopitchme: " + idea.title
						url = config.SITE_URL + "/idea/" + str(idea.key().id())
						tweet = generate_tweet(text, url)
						
						response = "Feedback sent"
						call_to_action = "Why not tweeting this idea to your friends?"
						values = {
							"response": response,
							"call_to_action": call_to_action,
							"tweet": tweet,
							"skip_url": "/idea/" + str(idea.key().id()),
						}
						path = "idea/tweet.html"
					else:
						values = {
							"response": "Thanks for your feedback",
							"next": {
								"content": "Back",
								"url": "/idea/"+str(idea.key().id()),
							}
						}	
						path = "feedback.html"
					
					self.render(path, values)
				else:
					raise GetpitchdError("Feedback already sent")
			else:
				raise GetpitchdError("Forbidden feedback")
		else:
			raise GetpitchdError("Idea does not exist")
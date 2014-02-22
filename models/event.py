import json

from google.appengine.api.taskqueue import Task

from controllers import config

from models.idea import Idea
from models.user import User
from models.comment import Comment

class Event():
	def send(self):
		self._data.update({
			"site_url": config.SITE_URL,
			"img_url": config.IMG_URL,
		})
		
		task = Task(
			url="/queue/event",
			params={
				"name": self._name,
				"data": json.dumps(self._data)
			}
		)
		task.add(queue_name="events-queue")

class IdeaCommentEvent(Event):
	def __init__(self, user, comment, idea):
		self._name = "idea:comment"
		
		author_key = Idea.author.get_value_for_datastore(idea)
		author = User.get(author_key)
		
		if(author.email_idea_comment):
			self._data = {
				"user": {
					"id": user.key().id(),
				},
				"comment":{
					"id": comment.key().id(),
					"text": comment.text,
				},
				"idea": {
					"id": idea.key().id(),
					"title": idea.title,
					"author": {
						"username": author.username,
						"name": author.name,
						"email": author.email,
					},
					"positive": idea.positive,
					"negative": idea.negative,
					"comments": idea.comments,
				}
			}
			self.send()

class CommentReplyEvent(Event):
	def __init__(self, user, reply, comment):
		self._name = "comment:reply"

		author_key = Comment.author.get_value_for_datastore(comment)
		author = User.get(author_key)
		
		if(author.email_comment_reply):
			self._data = {
				"user": {
					"id": user.key().id(),
				},
				"reply":{
					"id": reply.key().id(),
					"text": reply.text,
				},
				"comment": {
					"id": comment.key().id(),
					"author": {
						"username": author.username,
						"name": author.name,
						"email": author.email,
					}
				},
			}
			self.send()

class IdeaFeedbackEvent(Event):
	def __init__(self, user, feedback, idea, comment=None):
		self._name = "idea:feedback"
		
		author_key = Idea.author.get_value_for_datastore(idea)
		author = User.get(author_key)
		
		if(author.email_idea_feedback):
			self._data = {
				"user": {
					"id": user.key().id(),
				},
				"feedback": {
					"id": feedback.key().id(),
					"content": feedback.content,
					"comment": comment,
				},
				"idea":{
					"id": idea.key().id(),
					"title": idea.title,
					"author": {
						"username": author.username,
						"name": author.name,
						"email": author.email,
					},
					"positive": idea.positive,
					"negative": idea.negative,
					"comments": idea.comments,
				}
			}
			self.send()

from google.appengine.ext import db

from models.user import User
from models.idea import Idea

class Feedback(db.Model):
	author = db.ReferenceProperty(User, required=True, collection_name="feedbackAuthor")
	idea = db.ReferenceProperty(Idea, required=True, collection_name="feedbackIdea")
	content = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)
	updated = db.DateTimeProperty(auto_now = True)
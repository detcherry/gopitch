from google.appengine.ext import db

from models.user import User
from models.idea import Idea

class Comment(db.Model):
	idea = db.ReferenceProperty(Idea, required=True, collection_name="commentIdea")
	author = db.ReferenceProperty(User, required=True, collection_name="commentAuthor")
	text = db.TextProperty(required=True)
	reply_to = db.SelfReferenceProperty(collection_name="commentReplyto")
	created = db.DateTimeProperty(auto_now_add = True)
	updated = db.DateTimeProperty(auto_now = True)
  
	
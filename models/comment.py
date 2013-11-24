from google.appengine.ext import db

from models.user import User
from models.idea import Idea

class Comment(db.Model):
	author = db.ReferenceProperty(User, required=True, collection_name="commentAuthor")
	text = db.TextProperty(required=True)
	reply_to = db.SelfReferenceProperty(collection_name="commentReplyto")
	depth = db.IntegerProperty(default=0, indexed=False)
	created = db.DateTimeProperty(auto_now_add = True)
	updated = db.DateTimeProperty(auto_now = True)
  
	
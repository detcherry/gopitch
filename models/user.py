from google.appengine.ext import db

class User(db.Model):
	# keyname = twitter id
	username = db.StringProperty(required = True)
	name = db.StringProperty(required = True)
	access_token_key = db.StringProperty(required = True)
	access_token_secret = db.StringProperty(required = True)
	email = db.EmailProperty(required = False)
	created = db.DateTimeProperty(auto_now_add = True)
	updated = db.DateTimeProperty(auto_now = True)
from google.appengine.ext import db

class Pitch(db.Model):
	title = db.StringProperty(required = True)
	author = db.ReferenceProperty(required = True)
	answers = db.StringListProperty(required = True)
	version = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	updated = db.DateTimeProperty(auto_now = True)
	

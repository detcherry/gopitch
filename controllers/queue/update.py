import logging

from google.appengine.ext import db
from google.appengine.api.taskqueue import Task

from controllers.base import BaseHandler

from models.user import User

class QueueUpdateHandler(BaseHandler):
	def post(self):
		cursor = self.request.get("cursor")
		
		q = User.all()
		q.order("created")
		
		# Is there a cursor?
		if(cursor):
			logging.info("Cursor found")
			q.with_cursor(start_cursor = cursor)
		else:
			logging.info("No cursor")
		
		batch_size = 50
		users = q.fetch(batch_size)
		
		for user in users:
			if user.img:
				del user.img
				
		db.put(users)
		
		if(len(users)==batch_size):
			new_cursor = q.cursor()
			task = Task(
				url = "/queue/update",
				params = {
					'cursor': new_cursor,
				},
				countdown = 10,
			)
			task.add()
			
			logging.info("New task started")
		else:
			logging.info("No more task to create")
			
		
		
		
		
		
		

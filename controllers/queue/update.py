import logging

import cloudstorage as gcs

from tweepy import auth
from tweepy import TweepError
from tweepy.api import API

from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import blobstore
from google.appengine.api import images
from google.appengine.api.taskqueue import Task

from controllers import config
from controllers.base import BaseHandler

from models.user import User
from models.idea import Idea

class QueueUpdateHandler(BaseHandler):
	def post(self):
		cursor = self.request.get("cursor")
		
		q = Idea.all()
		q.order("created")
		
		# Is there a cursor?
		if(cursor):
			logging.info("Cursor found")
			q.with_cursor(start_cursor = cursor)
		else:
			logging.info("No cursor")


		"""
		batch_size = 5
		ideas = q.fetch(batch_size)
		new_ideas = []

		for idea in ideas:
			problem = idea.answers[0]
			solution = idea.answers[1]
			competitors = idea.answers[3]
			business_model = idea.answers[4]
			acquisition = idea.answers[5]
			milestones = idea.answers[6]
			
			new_answers = [
				problem,
				solution,
				acquisition,
				business_model,
				competitors,
				milestones,
			]
			idea.answers = new_answers
			idea.version = "1"
			new_ideas.append(idea)

		db.put(new_ideas)

		for user in users:
			try:
				del user.image
			except:
				logging.info("there was a pb")

			try:
				del user.img
			except:
				logging.info("there was a pb 2")

		db.put(users)
		
		##########

		if(len(users)>0):
			user = users[0]

			logging.info(user.username)

			filename = config.FOLDER + "/" + str(user.twitter_id)
			gcs_file = gcs.open(filename,'w',content_type="image",options={"x-goog-acl":"public-read"})
			gcs_file.write(user.image)
			gcs_file.close()
		"""

		if(len(ideas)==batch_size):
			new_cursor = q.cursor()
			task = Task(
				url = "/queue/update",
				params = {
					'cursor': new_cursor,
				},
				countdown = 2,
			)
			task.add(queue_name="update-queue")
			
			logging.info("New task started")
		else:
			logging.info("No more task to create")
			
		
		
		
		
		
		

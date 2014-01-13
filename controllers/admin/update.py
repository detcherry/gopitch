import logging

from google.appengine.api.taskqueue import Task

from controllers.base import BaseHandler
from controllers.base import admin_required

class AdminUpdateHandler(BaseHandler):
	@admin_required
	def get(self):
		self.render("admin.html", None)
	
	@admin_required
	def post(self):
		task = Task(url = "/queue/update", countdown=10)
		task.add(queue_name="update-queue")		
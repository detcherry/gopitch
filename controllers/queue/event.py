import logging
import json

from customerio import CustomerIO

from controllers.base import BaseHandler
from controllers import config

class QueueEventHandler(BaseHandler):
	def post(self):
		name = self.request.get("name")
		data = json.loads(self.request.get("data"))
		
		logging.info("customer.io event %s"%(name))
		
		cio = CustomerIO(config.CIO_SITE_ID, config.CIO_API_KEY)
		cio.track(data["user"]["id"], name, **data)
		
		
		
		

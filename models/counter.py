import random

from google.appengine.ext import db

class Shard(db.Model):
	num = db.IntegerProperty(required=True, default=10)
	
	@staticmethod
	def get_count(name):
		total = 0
		for counter in Counter.all().filter('name = ', name):
			total += counter.count

		return total

	@staticmethod
	def update(name, value):
		shard = Shard.get_or_insert(name)
		def txn():
			index = random.randint(0, shard.num - 1)
			counter_name = name + str(index)
			counter = Counter.get_by_key_name(counter_name)
			if counter is None:
				counter = Counter(key_name=counter_name, name=name)
			counter.count += value
			counter.put()
		db.run_in_transaction(txn)	

	@staticmethod
	def increment(name):
		Shard.update(name, 1)

	@staticmethod
	def decrement(name):
		Shard.update(name, -1)


class Counter(db.Model):
	name = db.StringProperty(required=True)
	count = db.IntegerProperty(required=True, default=0)
	

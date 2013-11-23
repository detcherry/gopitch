import logging

from google.appengine.ext import db

from models.user import User
from models.counter import Shard

class Idea(db.Model):
	title = db.StringProperty(required=True)
	author = db.ReferenceProperty(User, required=True, collection_name="ideaAuthor")
	answers = db.StringListProperty(required=True)
	version = db.StringProperty(required=True)
	positive = db.IntegerProperty(required=True, default=0)
	negative = db.IntegerProperty(required=True, default=0)
	score = db.FloatProperty(required=True, default=0.0)
	country = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	updated = db.DateTimeProperty(auto_now=True)

	@staticmethod
	def get_steps(version):
		steps = []
		
		if(version == "0"):
			steps = [{
				"slug": "problem",
				"title": "Problem",
				"question": "What is the problem you're trying to solve? Who has this problem?",
			},{
				"slug": "solution",
				"title": "Solution",
				"question": "What are you going to build?",
			},{
				"slug": "opportunity",
				"title": "Opportunity",
				"question": "What's new about what you're building? What are people forced to do because you don't exist?",
			},{
				"slug": "competitors",
				"title": "Competitors",
				"question": "Who are your competitors?",
			},{
				"slug": "business_model",
				"title": "Business Model",
				"question": "How are you going to make money?",
			},{
				"slug": "acquisition",
				"title": "Acquisition",
				"question": "How will potential users know about you?",
			},{
				"slug": "milestones",
				"title": "Milestones",
				"question": "Are you posting this idea for fun or would you like to dig into it? Find a cofounder?",
			}]
		else:
			logging.error("Idea version does not exist...")
		
		return steps
	
	@staticmethod
	def get_extended_idea(idea):
		extended_steps = []
		steps = Idea.get_steps(idea.version)

		for i in range(len(steps)):
			title = steps[i]["title"]
			question = steps[i]["question"]
			answer = idea.answers[i]

			extended_steps.append({
				"title": title,
				"question": question,
				"answer": answer,
			})
			
		extended_idea = {
			"id": idea.key().id(),
			"title": idea.title,
			"positive": idea.positive,
			"negative": idea.negative,
			"extended_steps": extended_steps,
		}
		
		return extended_idea

				
		
		
		
			
		
		
	

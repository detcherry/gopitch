def generate_tweet(text, url):
	short_url_length = 22 # See https://dev.twitter.com/docs/api/1.1/get/help/configuration
	tweet = text
	
	characters_left = 140 - len(" ") - short_url_length
	if len(tweet) < characters_left:
		tweet = tweet + " "
	else:
		tweet = tweet[:characters_left-3] + "..." + " "
	
	tweet += url
	
	return tweet
import webapp2

from controllers.home import HomeHandler
from controllers.auth import AuthSigninHandler
from controllers.auth import AuthCallbackHandler
from controllers.auth import AuthSignoutHandler
from controllers.auth import AuthCompleteHandler
from controllers.idea.pitch import IdeaPitchHandler
from controllers.idea.idea import IdeaHandler

config = {}
config["webapp2_extras.sessions"] = {
	"secret_key": "getp1tchd!",
}

app = webapp2.WSGIApplication(
	[
		("/auth/signin", AuthSigninHandler),
		("/auth/callback", AuthCallbackHandler),		
		("/auth/signout", AuthSignoutHandler),
		("/auth/complete", AuthCompleteHandler),
		("/idea/pitch", IdeaPitchHandler),
		("/idea/([0-9]+)", IdeaHandler),
		("/.*", HomeHandler),
	],
	config = config,
	debug = True,
)
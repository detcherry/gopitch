import webapp2

from controllers.home import HomeHandler
from controllers.auth import AuthSigninHandler
from controllers.auth import AuthCallbackHandler
from controllers.auth import AuthSignoutHandler
from controllers.auth import AuthCompleteHandler
from controllers.pitch import PitchCreateHandler

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
		("/pitch/create", PitchCreateHandler),
		("/.*", HomeHandler),
	],
	config = config,
	debug = True,
)
import webapp2

from controllers.home import HomeHandler
from controllers.auth import AuthSigninHandler
from controllers.auth import AuthCallbackHandler
from controllers.auth import AuthSignoutHandler

config = {}
config["webapp2_extras.sessions"] = {
	"secret_key": "getp1tchd!",
}

app = webapp2.WSGIApplication(
	[
		("/auth/signin", AuthSigninHandler),
		("/auth/callback", AuthCallbackHandler),		
		("/auth/signout", AuthSignoutHandler),
		("/.*", HomeHandler),
	],
	config = config,
	debug = True,
)
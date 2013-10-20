import webapp2

from controllers.main import HomeHandler
from controllers.main import OauthTwitterSigninHandler
from controllers.main import OauthTwitterCallbackHandler

config = {}
config["webapp2_extras.sessions"] = {
	"secret_key": "getp1tchd!",
}

app = webapp2.WSGIApplication(
	[
		("/oauth/twitter/signin", OauthTwitterSigninHandler),
		("/oauth/twitter/callback", OauthTwitterCallbackHandler),
		("/.*", HomeHandler),
	],
	config = config,
	debug = True,
)
import webapp2

from controllers.home import HomeHandler
from controllers.auth import AuthSigninHandler
from controllers.auth import AuthCallbackHandler
from controllers.auth import AuthSignoutHandler
from controllers.auth import AuthCompleteHandler
from controllers.idea.pitch import IdeaPitchHandler
from controllers.idea.idea import IdeaHandler
from controllers.idea.edit import IdeaEditHandler
from controllers.idea.delete import IdeaDeleteHandler
from controllers.idea.feedback import IdeaFeedbackHandler
from controllers.idea.comment import IdeaCommentHandler
from controllers.comment.reply import CommentReplyHandler
from controllers.comment.delete import CommentDeleteHandler
from controllers.feedback.delete import FeedbackDeleteHandler
from controllers.user.user import UserHandler
from controllers.user.tweet import UserTweetHandler

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
		("/idea/([0-9]+)/edit", IdeaEditHandler),
		("/idea/([0-9]+)/delete", IdeaDeleteHandler),
		("/idea/([0-9]+)/feedback", IdeaFeedbackHandler),
		("/idea/([0-9]+)/comment", IdeaCommentHandler),
		("/comment/([0-9]+)/reply", CommentReplyHandler),
		("/comment/([0-9]+)/delete", CommentDeleteHandler),
		("/feedback/([0-9_]+)/delete", FeedbackDeleteHandler),
		("/user/tweet", UserTweetHandler),
		("/(\w+)", UserHandler),
		("/.*", HomeHandler),
	],
	config = config,
	debug = True,
)
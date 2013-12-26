import os

# Necessary for templates
PROJECT_ROOT = os.path.dirname(__file__)
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

# Necessary for custom tags
INSTALLED_APPS = ('ext')
from .utils import env


def show_toolbar(request):
    if DEBUG == "1":
        return False  # Toolbar is turned off by default for all environments. Set this to True if needed. It can generate too much content in the page and isn't always useful.


# False if not in os.environ because of casting above
DEBUG = env("DEBUG")

if DEBUG == "1":
    DEBUG = True
else:
    DEBUG = False

INTERNAL_IPS = (
    "127.0.0.1",
    "localhost",
)

# Test Suite
ADD_TEST_OBJECTS = DEBUG  # Adds testing objects like users and projects
ADD_TEST_PROJECTS = DEBUG  # Adds test projects


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

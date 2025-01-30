from .utils import env

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s.%(funcName)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",  # Ensure DEBUG level messages are logged to console
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("ROOT_LOG_LEVEL"),  # Default to INFO for general logging
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",  # INFO level for general Django messages
            "propagate": True,
        },
        # "transformations": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",  # DEBUG level for the transformations logger
        #     "propagate": True,
        # },
        # "mozilla_django_oidc": {
        #     "handlers": ["console"],
        #     "level": "DEBUG",  # DEBUG level for Mozilla OIDC
        # },
    },
}

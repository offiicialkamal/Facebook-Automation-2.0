"""
Configuration for Facebook Comment Bot
"""

# Default cookie strings (replace with your own)
DEFAULT_COOKIES = [
    # Cookie 1 (Main account)
    "datr=SK8maRcMTTI5l5jYA2lNg9Vn; fr=10DTXgNJyOhjXXbVl.AWeWqJ_2gegQvWxTZiom95bjeXBPptBTlF70DcjGHpH3AM3dQ-A.BpRmyz..AAA.0.0.BpRmyz.AWdLi3KMi0AE8WbFy3tk_NlpQ1w; sb=SK8maQT5FcoNhX1ii3_svYfg; locale=en_US; wd=588x479; dpr=1.6800000667572021; ps_l=1; ps_n=1; c_user=100086111536900; xs=4%3AhEP3GPso2CzlRA%3A2%3A1766136688%3A-1%3A-1%3A%3AAczQc-ROIT3b9-QsJ-ly1BG_JahRSenkLut1oe9Jcw; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1766223040399%2C%22v%22%3A1%7D",

    # Add more cookies here
    # "cookie_string_2",
    # "cookie_string_3",
]

# Default values
DEFAULT_POST_URL = "https://www.facebook.com/100068994467075/posts/534891072154037/"
DEFAULT_COMMENT_TEXT = "Lightning fast comment! ⚡"
DEFAULT_TOTAL_COMMENTS = 10
DEFAULT_MAX_WORKERS = 8

# Timeouts (in seconds)
GRAPH_API_TIMEOUT = 3
WEB_GRAPHQL_TIMEOUT = 3
SESSION_TIMEOUT = 10
INITIALIZATION_TIMEOUT = 30

# Retry settings
MAX_RETRIES = 2
RETRY_DELAY = 0.5

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(asctime)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'facebook_bot.log',
            'level': 'DEBUG'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

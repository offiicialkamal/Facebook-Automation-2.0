"""
Facebook Comment Bot - Lightning-fast parallel commenting
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Ultimate Facebook Comment Bot with parallel processing"

from .bot import LightningCommentBot
from .session import FacebookSession
from .cli import CLI
from .models import CommentResult, Profile, BotStats, SessionStatus

__all__ = [
    'LightningCommentBot',
    'FacebookSession',
    'CLI',
    'CommentResult',
    'Profile',
    'BotStats',
    'SessionStatus'
]
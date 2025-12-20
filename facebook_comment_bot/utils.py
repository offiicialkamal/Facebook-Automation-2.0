"""
Utility functions for the Facebook Comment Bot
"""

import re
import json
import base64
import uuid
import random
import time
from typing import Dict, Optional, List, Tuple
from urllib.parse import quote
import logging

logger = logging.getLogger(__name__)

def parse_cookies(cookie_string: str) -> Dict:
    """Parse cookie string into dictionary"""
    cookies = {}
    for item in cookie_string.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key] = value
    return cookies

def extract_post_id(post_url: str) -> Optional[str]:
    """Extract post ID from Facebook URL"""
    patterns = [
        r'/posts/(\d+)',
        r'story_fbid=(\d+)',
        r'fbid=(\d+)',
        r'(\d{15,})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, post_url)
        if match:
            return match.group(1)
    return None

def generate_comment_text(base_text: str, attempt_num: int = 1) -> str:
    """Generate comment text with variation"""
    if attempt_num == 1:
        return base_text
    
    emojis = ['👍', '😊', '🙏', '🔥', '⭐', '💯', '🎯', '🚀', '⚡', '✨']
    variation = random.choice(emojis)
    return f"{base_text} {variation}"

def get_feedback_id(post_id: str) -> str:
    """Get feedback ID for GraphQL requests"""
    return base64.b64encode(f"feedback:{post_id}".encode()).decode()

def calculate_jazoest(token: str) -> str:
    """Calculate jazoest value for Facebook requests"""
    return str(sum(ord(c) for c in token) % 100000)

def format_time(seconds: float) -> str:
    """Format time in human-readable format"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = seconds / 60
        return f"{minutes:.1f}m"

def print_progress(current: int, total: int, prefix: str = "", suffix: str = ""):
    """Print progress bar"""
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    percent = (current / total) * 100
    
    # Clear line and print progress
    print(f'\r{prefix} |{bar}| {percent:.1f}% {suffix}', end='', flush=True)
    
    if current == total:
        print()
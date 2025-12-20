"""
Data models for the Facebook Comment Bot
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class CommentResult:
    """Result of a comment attempt"""
    success: bool
    session_id: str
    profile_name: str
    profile_type: str
    attempt_num: int
    method: str
    comment_id: Optional[str] = None
    error: Optional[str] = None
    elapsed: float = 0.0
    timestamp: float = 0.0

@dataclass
class Profile:
    """Facebook profile (user or page)"""
    id: str
    name: str
    type: str  # 'user' or 'page'
    token_type: str
    access_token: Optional[str] = None

@dataclass
class SessionStatus:
    """Session status information"""
    session_id: str
    user_id: str
    initialized: bool
    login_time: float
    profiles_count: int
    has_eaag_token: bool
    has_web_token: bool
    pages_count: int

@dataclass
class BotStats:
    """Bot statistics"""
    total_comments: int
    successful: int
    failed: int
    speed: float  # comments/second
    total_time: float
    sessions_used: int
    profiles_used: int
    parallel_workers: int
    start_time: float
    end_time: float
"""
Facebook Session class for managing individual accounts
"""

import re
import json
import time
import requests
from typing import Dict, Tuple, List, Optional
import logging

from .models import Profile, SessionStatus
from .utils import parse_cookies, get_feedback_id, calculate_jazoest, generate_comment_text

logger = logging.getLogger(__name__)

class FacebookSession:
    """Represents a single authenticated Facebook session"""
    
    def __init__(self, session_id: str, cookie_string: str):
        self.session_id = session_id
        self.cookies = parse_cookies(cookie_string)
        self.user_id = self.cookies.get('c_user')
        
        if not self.user_id:
            raise ValueError("No c_user found in cookies")
        
        # Session
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        
        # Authentication
        self.fb_dtsg = None
        self.eaag_token = None
        self.page_tokens = {}
        self.profiles: List[Profile] = []
        
        # Status
        self.initialized = False
        self.login_time = None
        
    def initialize(self) -> bool:
        """Initialize session - login and get tokens"""
        try:
            logger.info(f"🔐 Logging in {self.session_id}...")
            
            # Get EAAG token
            self._get_eaag_token()
            
            # Get web token
            self._get_web_token()
            
            # Get pages if EAAG token exists
            if self.eaag_token:
                self._get_pages()
            
            # Prepare profiles
            self._prepare_profiles()
            
            self.initialized = True
            self.login_time = time.time()
            
            logger.info(f"✅ {self.session_id} ready ({len(self.profiles)} profiles)")
            return True
            
        except Exception as e:
            logger.error(f"❌ {self.session_id} failed: {e}")
            return False
    
    def _get_eaag_token(self):
        """Get EAAG token from business.facebook.com"""
        try:
            url = "https://business.facebook.com/business_locations"
            response = self.session.get(url, timeout=10)
            match = re.search(r'(\["EAAG\w+)', response.text)
            if match:
                self.eaag_token = match.group(1).replace('["', '')
                logger.info(f"  ✅ EAAG token obtained")
        except Exception as e:
            logger.info(f"  ⚠️ EAAG token failed: {e}")
    
    def _get_web_token(self):
        """Get web token (fb_dtsg)"""
        try:
            response = self.session.get('https://www.facebook.com/?sk=h_chr', timeout=10)
            html = response.text
            patterns = [
                r'"DTSGInitData",\[\],{"token":"([^"]+)"',
                r'name="fb_dtsg" value="([^"]+)"',
                r'"fb_dtsg":"([^"]+)"',
            ]
            for pattern in patterns:
                match = re.search(pattern, html)
                if match:
                    self.fb_dtsg = match.group(1)
                    logger.info(f"  ✅ Web token obtained")
                    break
        except Exception as e:
            logger.info(f"  ⚠️ Web token failed: {e}")
    
    def _get_pages(self):
        """Get pages via Graph API"""
        try:
            url = f"https://graph.facebook.com/me/accounts?access_token={self.eaag_token}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            if "data" in data:
                for account in data["data"]:
                    self.page_tokens[account["id"]] = {
                        "name": account.get("name", f"Page {account['id']}"),
                        "access_token": account.get("access_token", ""),
                        "category": account.get("category", ""),
                    }
                logger.info(f"  ✅ {len(self.page_tokens)} pages found")
        except Exception as e:
            logger.info(f"  ⚠️ No pages: {e}")
    
    def _prepare_profiles(self):
        """Prepare list of available profiles"""
        # Add main user
        self.profiles.append(Profile(
            id=self.user_id,
            name=f"User_{self.user_id[:6]}",
            type="user",
            token_type="EAAG" if self.eaag_token else "Web",
            access_token=self.eaag_token if self.eaag_token else None
        ))
        
        # Add pages
        for page_id, page_info in self.page_tokens.items():
            self.profiles.append(Profile(
                id=page_id,
                name=page_info["name"],
                type="page",
                token_type="PageToken",
                access_token=page_info["access_token"]
            ))
    
    def get_status(self) -> SessionStatus:
        """Get session status"""
        return SessionStatus(
            session_id=self.session_id,
            user_id=self.user_id,
            initialized=self.initialized,
            login_time=self.login_time,
            profiles_count=len(self.profiles),
            has_eaag_token=bool(self.eaag_token),
            has_web_token=bool(self.fb_dtsg),
            pages_count=len(self.page_tokens)
        )
    
    def post_comment(self, post_id: str, comment_text: str, 
                     use_profile: Optional[Profile] = None, 
                     attempt_num: int = 1) -> Tuple[bool, str, str, float]:
        """
        Post a comment using available methods
        
        Returns: (success, comment_id/error, method, elapsed_time)
        """
        start_time = time.time()
        
        # Use main profile if not specified
        if not use_profile:
            use_profile = self.profiles[0]
        
        # Generate comment with variation
        final_comment = generate_comment_text(comment_text, attempt_num)
        
        # METHOD 1: Graph API (preferred - fastest)
        if use_profile.access_token:
            success, comment_id, error = self._graph_api_comment(
                post_id, final_comment, use_profile.access_token)
            if success:
                elapsed = time.time() - start_time
                return True, comment_id, "GraphAPI", elapsed
        
        # METHOD 2: Web GraphQL (fallback)
        if self.fb_dtsg:
            success, comment_id, error = self._web_graphql_comment(
                post_id, final_comment, use_profile.id)
            if success:
                elapsed = time.time() - start_time
                return True, comment_id, "WebGraphQL", elapsed
        
        elapsed = time.time() - start_time
        return False, error, "Failed", elapsed
    
    def _graph_api_comment(self, post_id: str, comment_text: str, token: str) -> Tuple[bool, str, str]:
        """Comment via Graph API"""
        try:
            from urllib.parse import quote
            encoded_comment = quote(comment_text)
            url = f"https://graph.facebook.com/{post_id}/comments?message={encoded_comment}&access_token={token}"
            
            response = self.session.post(url, timeout=3)  # Short timeout for speed
            data = response.json()
            
            if "id" in data:
                return True, data["id"], ""
            else:
                error = data.get("error", {}).get("message", "Unknown")
                return False, "", f"GraphAPI: {error}"
        except Exception as e:
            return False, "", f"GraphAPI: {str(e)[:30]}"
    
    def _web_graphql_comment(self, post_id: str, comment_text: str, actor_id: str) -> Tuple[bool, str, str]:
        """Comment via Web GraphQL"""
        if not self.fb_dtsg:
            return False, "", "No web token"
        
        try:
            feedback_id = get_feedback_id(post_id)
            jazoest = calculate_jazoest(self.fb_dtsg)
            
            data = {
                'av': actor_id,
                '__user': actor_id,
                '__a': '1',
                '__req': '1',
                'fb_dtsg': self.fb_dtsg,
                'jazoest': jazoest,
                'variables': json.dumps({
                    "input": {
                        "feedback_id": feedback_id,
                        "message": {"text": comment_text},
                        "actor_id": actor_id,
                        "client_mutation_id": str(uuid.uuid4())[:8],
                    },
                    "scale": 1,
                }),
                'doc_id': '24615176934823390',
            }
            
            response = self.session.post(
                'https://www.facebook.com/api/graphql/',
                data=data,
                timeout=3  # Short timeout
            )
            
            if response.status_code == 200 and '"comment_create"' in response.text:
                # Extract comment ID
                match = re.search(r'"comment_id":"([^"]+)"', response.text)
                comment_id = match.group(1) if match else "unknown"
                return True, comment_id, ""
            else:
                return False, "", f"HTTP:{response.status_code}"
                
        except Exception as e:
            return False, "", f"WebGraphQL: {str(e)[:30]}"
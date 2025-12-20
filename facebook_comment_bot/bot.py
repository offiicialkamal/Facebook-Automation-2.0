"""
Main Facebook Comment Bot class with parallel processing
"""

import time
import threading
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import logging

from .session import FacebookSession
from .models import CommentResult, BotStats
from .utils import extract_post_id, print_progress

logger = logging.getLogger(__name__)

class LightningCommentBot:
    """Lightning-fast comment bot with pre-login and parallel processing"""
    
    def __init__(self, cookie_strings: List[str]):
        """
        Initialize with multiple cookie strings
        
        Args:
            cookie_strings: List of cookie strings for different accounts
        """
        self.sessions: List[FacebookSession] = []
        self.ready_sessions: List[FacebookSession] = []
        self.total_profiles = 0
        
        self._initialize_sessions(cookie_strings)
        
        if not self.ready_sessions:
            raise ValueError("No valid sessions initialized")
    
    def _initialize_sessions(self, cookie_strings: List[str]):
        """Initialize all sessions in parallel"""
        print("\n" + "="*70)
        print("🚀 LIGHTNING COMMENT BOT - PRE-LOGIN PHASE")
        print("="*70)
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            
            for i, cookie_str in enumerate(cookie_strings):
                session_id = f"Session_{i+1}"
                future = executor.submit(self._create_session, session_id, cookie_str)
                futures.append(future)
            
            # Initialize sessions with progress
            completed = 0
            total = len(futures)
            
            for future in as_completed(futures):
                try:
                    session = future.result()
                    if session:
                        self.ready_sessions.append(session)
                        self.total_profiles += len(session.profiles)
                    
                    completed += 1
                    print_progress(completed, total, "Logging in sessions", 
                                 f"{completed}/{total}")
                except Exception as e:
                    logger.error(f"Session failed: {e}")
                    completed += 1
        
        print("="*70)
        print(f"✅ PRE-LOGIN COMPLETE: {len(self.ready_sessions)} sessions, {self.total_profiles} profiles")
        print("="*70)
    
    def _create_session(self, session_id: str, cookie_str: str) -> Optional[FacebookSession]:
        """Create and initialize a session"""
        try:
            session = FacebookSession(session_id, cookie_str)
            if session.initialize():
                return session
        except Exception as e:
            logger.error(f"{session_id} creation failed: {e}")
        return None
    
    def get_status(self) -> Dict:
        """Get bot status information"""
        status = {
            "sessions_count": len(self.ready_sessions),
            "total_profiles": self.total_profiles,
            "sessions": []
        }
        
        for session in self.ready_sessions:
            session_status = session.get_status()
            status["sessions"].append({
                "id": session_status.session_id,
                "user_id": session_status.user_id,
                "profiles": session_status.profiles_count,
                "pages": session_status.pages_count,
                "has_eaag": session_status.has_eaag_token,
                "has_web": session_status.has_web_token,
            })
        
        return status
    
    def rapid_comments(self, post_url: str, comment_text: str, 
                       total_comments: int = 10, max_workers: int = 10) -> Dict:
        """
        Lightning-fast parallel commenting
        
        Args:
            post_url: Facebook post URL
            comment_text: Comment text
            total_comments: Total comments to post
            max_workers: Maximum number of parallel workers
        
        Returns:
            Results dictionary
        """
        # Extract post ID
        post_id = extract_post_id(post_url)
        if not post_id:
            return {"error": "Invalid post URL"}
        
        print("\n" + "="*70)
        print("⚡ LIGHTNING COMMENTING STARTED")
        print("="*70)
        print(f"🎯 Target: {total_comments} comments")
        print(f"🧵 Parallel workers: {max_workers}")
        print("="*70)
        
        # Prepare results
        results_queue = Queue()
        all_results = []
        results_lock = threading.Lock()
        
        start_time = time.time()
        
        # Use ThreadPoolExecutor for maximum parallelism
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            comment_counter = 1
            
            # Distribute comments across sessions and profiles
            comments_per_session = total_comments // len(self.ready_sessions)
            extra_comments = total_comments % len(self.ready_sessions)
            
            for session_idx, session in enumerate(self.ready_sessions):
                session_comments = comments_per_session + (1 if session_idx < extra_comments else 0)
                
                for i in range(session_comments):
                    # Round-robin through profiles
                    profile_idx = (comment_counter - 1) % len(session.profiles)
                    profile = session.profiles[profile_idx]
                    
                    future = executor.submit(
                        self._comment_worker,
                        session,
                        post_id,
                        comment_text,
                        profile,
                        comment_counter,
                        results_queue
                    )
                    futures.append(future)
                    comment_counter += 1
            
            # Collect results
            completed = 0
            successful = 0
            
            # Show initial progress
            print(f"\n🚀 Launching {len(futures)} parallel comments...")
            
            for future in as_completed(futures):
                try:
                    future.result()  # Just to raise any exceptions
                    completed += 1
                    
                    # Get result from queue
                    if not results_queue.empty():
                        result = results_queue.get()
                        with results_lock:
                            all_results.append(result)
                        
                        if result.success:
                            successful += 1
                            print(f"✅ {result.profile_name}: {result.method} ({result.elapsed:.2f}s)")
                        else:
                            print(f"❌ {result.profile_name}: {result.error[:20]}")
                    
                    # Show progress
                    if completed % max_workers == 0 or completed == total_comments:
                        print(f"📊 {completed}/{total_comments} ({successful} ✅)")
                
                except Exception as e:
                    print(f"⚠️ Error: {e}")
                    completed += 1
        
        # Calculate statistics
        total_time = time.time() - start_time
        
        # Prepare results dictionary
        stats = BotStats(
            total_comments=total_comments,
            successful=successful,
            failed=total_comments - successful,
            speed=successful / total_time if successful > 0 else 0,
            total_time=total_time,
            sessions_used=len(self.ready_sessions),
            profiles_used=self.total_profiles,
            parallel_workers=max_workers,
            start_time=start_time,
            end_time=time.time()
        )
        
        return {
            "stats": stats,
            "results": [{
                "session": r.session_id,
                "profile": r.profile_name,
                "type": r.profile_type,
                "attempt": r.attempt_num,
                "success": r.success,
                "method": r.method,
                "elapsed": round(r.elapsed, 3),
                "error": r.error
            } for r in all_results]
        }
    
    def _comment_worker(self, session: FacebookSession, post_id: str, 
                        comment_text: str, profile, attempt_num: int, 
                        results_queue: Queue):
        """Worker function for posting comments"""
        success, comment_id, method, elapsed = session.post_comment(
            post_id=post_id,
            comment_text=comment_text,
            use_profile=profile,
            attempt_num=attempt_num
        )
        
        result = CommentResult(
            success=success,
            session_id=session.session_id,
            profile_name=profile.name,
            profile_type=profile.type,
            attempt_num=attempt_num,
            method=method,
            comment_id=comment_id if success else None,
            error=None if success else comment_id,
            elapsed=elapsed,
            timestamp=time.time()
        )
        
        results_queue.put(result)
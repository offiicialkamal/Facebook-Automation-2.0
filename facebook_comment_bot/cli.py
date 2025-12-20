"""
Command Line Interface for the Facebook Comment Bot
"""

import sys
import time
from typing import List

from .bot import LightningCommentBot
from .utils import format_time

class CLI:
    """Command Line Interface handler"""
    
    def __init__(self, cookie_strings: List[str]):
        self.bot = None
        self.cookie_strings = cookie_strings
        
    def run(self):
        """Run the CLI"""
        self._print_header()
        
        try:
            # Initialize bot
            print("\n📥 Initializing bot...")
            self.bot = LightningCommentBot(self.cookie_strings)
            
            # Main loop
            while True:
                self._run_comment_session()
                
                # Ask if user wants to continue
                if not self._ask_continue():
                    break
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def _print_header(self):
        """Print application header"""
        print("\n" + "="*70)
        print("⚡ ULTIMATE FACEBOOK COMMENT BOT")
        print("="*70)
        print("🔥 Features:")
        print("  • Pre-login all sessions")
        print("  • Lightning-fast parallel commenting")
        print("  • Auto-fallback methods")
        print("  • Multi-account support")
        print("="*70)
    
    def _run_comment_session(self):
        """Run a comment session"""
        # Get user input
        post_url, comment_text, total_comments, max_workers = self._get_user_input()
        
        # Show configuration
        self._show_configuration(post_url, comment_text, total_comments, max_workers)
        
        # Wait for start command
        if not self._wait_for_start():
            return
        
        # Run comments
        self._run_lightning_comments(post_url, comment_text, total_comments, max_workers)
    
    def _get_user_input(self):
        """Get user input for commenting"""
        print("\n📝 Please provide comment details:")
        
        # Post URL
        default_post = "https://www.facebook.com/100068994467075/posts/534891072154037/"
        post_url = input(f"Enter post URL (default: {default_post[:50]}...): ").strip()
        if not post_url:
            post_url = default_post
            print(f"Using default post URL")
        
        # Comment text
        comment_text = input("Enter comment text: ").strip()
        if not comment_text:
            comment_text = "Lightning fast comment! ⚡"
            print(f"Using default: {comment_text}")
        
        # Number of comments
        try:
            total_comments = int(input("Number of comments to post (default: 10): ").strip() or "10")
        except:
            total_comments = 10
            print(f"Using default: {total_comments}")
        
        # Parallel workers
        try:
            max_workers = int(input("Parallel workers (default: 8): ").strip() or "8")
        except:
            max_workers = 8
            print(f"Using default: {max_workers}")
        
        return post_url, comment_text, total_comments, max_workers
    
    def _show_configuration(self, post_url: str, comment_text: str, 
                           total_comments: int, max_workers: int):
        """Show configuration summary"""
        print("\n" + "="*70)
        print("🎯 CONFIGURATION SUMMARY")
        print("="*70)
        print(f"Post URL: {post_url[:80]}...")
        print(f"Comment: {comment_text}")
        print(f"Target comments: {total_comments}")
        print(f"Parallel workers: {max_workers}")
        
        # Show bot status
        status = self.bot.get_status()
        print(f"Available sessions: {status['sessions_count']}")
        print(f"Available profiles: {status['total_profiles']}")
        print("="*70)
    
    def _wait_for_start(self) -> bool:
        """Wait for user to start commenting"""
        print("\n" + "="*70)
        print("⚡ READY TO FIRE")
        print("="*70)
        print("All sessions are pre-logged in and ready.")
        print("Comments will fire INSTANTLY when you press 'Y'")
        print("="*70)
        
        while True:
            cmd = input("\n🔥 Enter 'Y' to start commenting (or 'Q' to quit): ").strip().upper()
            
            if cmd == 'Q':
                return False
            elif cmd == 'Y':
                print("\n🔥 FIRING COMMENTS IN 3...")
                time.sleep(1)
                print("🔥 2...")
                time.sleep(1)
                print("🔥 1...")
                time.sleep(1)
                print("🔥 GO! ⚡\n")
                return True
            else:
                print("⚠️ Press 'Y' to start or 'Q' to quit")
    
    def _run_lightning_comments(self, post_url: str, comment_text: str, 
                               total_comments: int, max_workers: int):
        """Run lightning-fast commenting"""
        overall_start = time.time()
        
        # Run comments
        results = self.bot.rapid_comments(
            post_url=post_url,
            comment_text=comment_text,
            total_comments=total_comments,
            max_workers=max_workers
        )
        
        overall_time = time.time() - overall_start
        
        # Show results
        self._show_results(results, overall_time)
    
    def _show_results(self, results: dict, overall_time: float):
        """Show results summary"""
        stats = results.get('stats', {})
        
        print("\n" + "="*70)
        print("🎯 MISSION COMPLETE")
        print("="*70)
        print(f"✅ Successful: {stats.successful}/{stats.total_comments}")
        print(f"❌ Failed: {stats.failed}")
        print(f"⚡ Speed: {stats.speed:.2f} comments/second")
        print(f"⏱️  Commenting time: {format_time(stats.total_time)}")
        print(f"⏱️  Overall time: {format_time(overall_time)}")
        print(f"🧵 Workers used: {stats.parallel_workers}")
        
        if stats.speed >= 3:
            print("🏆 TARGET ACHIEVED! Lightning speed!")
        else:
            print(f"⚠️ Below target speed")
        
        # Show session breakdown
        print("\n📈 SESSION BREAKDOWN:")
        for session in self.bot.ready_sessions:
            session_results = [r for r in results['results'] if r['session'] == session.session_id]
            if session_results:
                session_success = sum(1 for r in session_results if r['success'])
                print(f"  {session.session_id}: {session_success}/{len(session_results)} successful")
        
        print("="*70)
    
    def _ask_continue(self) -> bool:
        """Ask if user wants to continue"""
        while True:
            again = input("\nRun again? (Y/N): ").strip().upper()
            if again == 'Y':
                return True
            elif again == 'N':
                print("\n👋 Session ended. Goodbye!")
                return False
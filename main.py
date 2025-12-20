#!/usr/bin/env python3
"""
Main entry point for Facebook Comment Bot
"""

import sys
import logging.config
from typing import List

from facebook_comment_bot.config import DEFAULT_COOKIES, LOGGING_CONFIG
from facebook_comment_bot.cli import CLI

def setup_logging():
    """Setup logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)

def load_cookies_from_file(filename: str = "cookies.txt") -> List[str]:
    """Load cookies from file"""
    try:
        with open(filename, 'r') as f:
            cookies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return cookies
    except FileNotFoundError:
        print(f"⚠️ Cookie file '{filename}' not found. Using default cookies.")
        return DEFAULT_COOKIES

def main():
    """Main entry point"""
    setup_logging()
    
    # Try to load cookies from file, otherwise use defaults
    cookies = load_cookies_from_file()
    
    if not cookies:
        print("❌ No cookies provided. Please add cookies to cookies.txt file or edit config.py")
        print("📁 Create a file named 'cookies.txt' and add your Facebook cookie strings (one per line)")
        sys.exit(1)
    
    print(f"📊 Loaded {len(cookies)} cookie strings")
    
    # Run CLI
    cli = CLI(cookies)
    cli.run()

if __name__ == "__main__":
    main()
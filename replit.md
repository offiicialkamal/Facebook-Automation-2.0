# Facebook Comment Bot

## Overview
A Python CLI tool for automating Facebook comments with parallel processing and multi-account support.

## Project Architecture
- `main.py` - Main entry point and CLI orchestration
- `core/` - Core bot functionality (bot.py, cli.py, session.py, models.py)
- `customs/` - Custom print utilities
- `essensials/` - JSON configuration files (colors, history, settings)
- `file_handlers/` - JSON and text file I/O utilities
- `general/` - Logo, user agent generator, post ID utilities
- `security/` - Module installer and security checks
- `updater/` - Update controller

## How to Run
This is a CLI application that runs in the console. Start the workflow and interact via the console panel.

The tool prompts for:
1. Cookie file path (text file with Facebook cookies)
2. Total comments count
3. Speed (1-10 recommended)
4. Comment text

## Dependencies
- Python 3.11
- requests - HTTP library for API calls
- art - ASCII art for logo display

## Configuration Files
- `essensials/settings.json` - Bot settings
- `essensials/history.json` - Session history
- `essensials/colors.json` - Color configuration

## Recent Changes
- January 2026: Initial import to Replit environment
- Fixed requirements.txt (removed invalid concurrent.futures entry)
- Installed Python 3.11 with required packages

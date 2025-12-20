import re
import requests

def get_numeric_post_id(fb_url: str):
    fb_url = fb_url.strip().split('#')[0]
    
    # If input is already just digits, return it
    if re.fullmatch(r'\d{10,}', fb_url):
        return fb_url
    
    # Check for numeric ID in the URL directly
    numeric_match = re.search(r'(\d{10,})', fb_url)
    if numeric_match:
        patterns_to_check = [
            r'/posts/\d{10,}',
            r'[?&]story_fbid=\d{10,}',
            r'[?&]fbid=\d{10,}',
            r'/permalink/\d{10,}',
            r'/groups/\d+/permalink/\d{10,}',
            r'/photos/[^/]+/\d{10,}',
            r'/videos/\d{10,}',
            r'/reel/\d{10,}',
            r'/story\.php\?story_fbid=\d{10,}',
        ]
        
        for pattern in patterns_to_check:
            if re.search(pattern, fb_url):
                return numeric_match.group(1)
    
    # For share URLs, follow redirects
    if '/share/p/' in fb_url:
        try:
            session = requests.Session()
            session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = session.get(fb_url, timeout=10, allow_redirects=True)
            final_url = response.url
            
            # SPECIAL CASE: Group permalink - extract POST ID (second number)
            group_permalink_match = re.search(r'/groups/(\d+)/permalink/(\d+)/', final_url)
            if group_permalink_match:
                # Return the POST ID (second number), not group ID
                return group_permalink_match.group(2)
            
            # Try to extract numeric ID from final URL with better patterns
            # Look for story_fbid parameter
            story_fbid_match = re.search(r'[?&]story_fbid=(\d{10,})', final_url)
            if story_fbid_match:
                return story_fbid_match.group(1)
            
            # Look for fbid parameter
            fbid_match = re.search(r'[?&]fbid=(\d{10,})', final_url)
            if fbid_match:
                return fbid_match.group(1)
            
            # Direct post patterns
            direct_post_match = re.search(r'/posts/(\d{10,})', final_url)
            if direct_post_match:
                return direct_post_match.group(1)
            
            # Permalink pattern (non-group)
            permalink_match = re.search(r'/permalink/(\d{10,})', final_url)
            if permalink_match:
                return permalink_match.group(1)
            
            # If redirected to login page, try to extract from the encoded URL
            if 'facebook.com/login/' in final_url:
                # Try to decode the next parameter
                import urllib.parse
                parsed = urllib.parse.urlparse(final_url)
                query = urllib.parse.parse_qs(parsed.query)
                if 'next' in query:
                    next_url = urllib.parse.unquote(query['next'][0])
                    # Try to extract from the next URL
                    next_story_match = re.search(r'[?&]story_fbid=(\d{10,})', next_url)
                    if next_story_match:
                        return next_story_match.group(1)
            
        except Exception as e:
            print(f"Error: {e}")
            pass
    
    # If we have a numeric match anywhere, return it as last resort
    if numeric_match:
        return numeric_match.group(1)
    
    return False
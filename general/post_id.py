import re
import requests


def get_numeric_post_id(url: str):
    """
    Extract numeric post ID from Facebook URL.
    Returns post ID (string) or False if not found.
    """
    url = url.strip()
    
    # If already a numeric ID, return it
    if re.fullmatch(r'\d{15,}', url):
        return url
    
    try:
        # Fetch the page
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        # Check HTML for post ID patterns
        patterns = [
            r'"post_id":"(\d{15,})"',
            r'"top_level_post_id":"(\d{15,})"',
            r'"feedbackTarget":"(\d{15,})"',
            r'"fbid":(\d{15,})',
            r'story_fbid=(\d{15,})',
            r'/posts/(\d{15,})',
            r'/permalink/(\d{15,})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        
        # Check URL as last resort
        match = re.search(r'(\d{15,})', url)
        if match:
            return match.group(1)
        
        return False
        
    except:
        # If network fails, try to extract from URL
        match = re.search(r'(\d{15,})', url)
        return match.group(1) if match else False

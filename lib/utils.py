import re
import json
from urllib.parse import urlparse

def extract_domain(url):
    """
    Extract the hostname (domain) from a URL.
    
    Args:
        url (str): The URL to parse.
        
    Returns:
        str|None: The hostname/domain from the URL, or None if parsing fails.
    """
    return urlparse(url).hostname
    
def parse_body(body_str):
    """
    Parse a string that might contain JSON data.
    
    Args:
        body_str (str): The string to parse, potentially containing JSON.
        
    Returns:
        dict|str|None:
            - Parsed JSON object (dict) if string contains valid JSON
            - Original string if not valid JSON
            - None if input is empty or None
    """
    if not body_str:
        return None
    try:
        return json.loads(body_str)
    except json.JSONDecodeError:
        return body_str
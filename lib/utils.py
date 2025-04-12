import re
import json
from urllib.parse import urlparse

def extract_domain(url):
    return urlparse(url).hostname
    
def parse_body(body_str):
    if not body_str:
        return None
    try:
        return json.loads(body_str)
    except json.JSONDecodeError:
        return body_str
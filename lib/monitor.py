import logging
import time
import requests
from datetime import datetime
from collections import defaultdict

from lib.utils import extract_domain, parse_body

logger = logging.getLogger("lib/monitor.py")

def check_health(endpoint):
    """
    Check the health status of a specified endpoint.
    
    Makes an HTTP request to the endpoint and determines if it's healthy based on:
    - HTTP status code (200-299 is considered healthy)
    - Response time (< 0.5 seconds is considered healthy)
    
    Args:
        endpoint (dict): Dictionary containing endpoint configuration with:
            - 'name': Endpoint name (required)
            - 'url': URL to check (required)
            - 'method': HTTP method to use (default: 'GET')
            - 'headers': HTTP headers to include (default: {})
            - 'body': Request body content (optional)
    
    Returns:
        str: "UP" if endpoint is healthy, "DOWN" otherwise
    """
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = parse_body(endpoint.get('body'))
    
    logger.debug(f"Checking health of {endpoint['name']} at {url}")
    
    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=1)
        response_time = time.time() - start_time
        
        if 200 <= response.status_code < 300 and response_time < 0.5:
            logger.debug(f"Endpoint {url} UP: status={response.status_code}, time={response_time:.3f}s")
            return "UP"
        else:
            logger.debug(f"Endpoint {url} DOWN: status={response.status_code}, time={response_time:.3f}s")
            return "DOWN"
    except requests.RequestException as e:
        logger.error(f"Request failed for {url}: {str(e)}")
        return "DOWN"


def monitor_endpoints(config):
    """
    Continuously monitor the health of multiple endpoints and their availability.
    
    Endpoints are checked in cycles with a target cycle time of 15 seconds.
    After each cycle, domain-based availability statistics are logged.
    
    Args:
        config (list): List of endpoint dictionaries, each containing:
            - 'url': URL to check (required)
            - Other parameters needed by check_health()
    
    Returns:
        This function runs in an infinite loop unitl keyboard interrupt signal
    """
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
    
    logger.debug("Starting monitoring")
    logger.debug(f"Monitoring {len(config)} endpoints")
    
    while True:
        cycle_start = time.time()
        logger.debug("Starting check cycle")
        
        for endpoint in config:
            domain = extract_domain(endpoint["url"])
            result = check_health(endpoint)
            
            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1
        
        logger.debug("Status check results:")
        for domain, stats in domain_stats.items():
            availability = int(100 * stats["up"] / stats["total"])
            logger.info(f"{domain} has {availability}% availability")
        
        logger.debug("Check cycle completed")
        
        cycle_duration = time.time() - cycle_start
        sleep_time = max(0, 15 - cycle_duration)
        logger.debug(f"Cycle took {cycle_duration:.2f}s, sleeping for {sleep_time:.2f}s")
        time.sleep(sleep_time)
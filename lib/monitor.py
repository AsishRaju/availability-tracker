import logging
import time
import requests
from datetime import datetime
from collections import defaultdict

from lib.utils import extract_domain, parse_body

logger = logging.getLogger("lib/monitor.py")

def check_health(endpoint):
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
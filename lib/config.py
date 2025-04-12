import yaml
import sys
import logging

from logging_config import setup_logging

logger = logging.getLogger("lib/config.py")

def load_config(file_path):
    try:
        logger.debug(f"Loading configuration from {file_path}")
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            if not isinstance(config, list):
                logger.error(f"YAML content should be a list of endpoints. Found: {type(config)}")
                sys.exit(1)
                
            logger.debug(f"Found {len(config)} endpoints in configuration")
            for i, endpoint in enumerate(config):
                if not isinstance(endpoint, dict):
                    logger.error(f"Endpoint entry #{i+1} is not a dictionary.")
                    sys.exit(1)
                if 'name' not in endpoint or not isinstance(endpoint['name'], str):
                    logger.error(f"Endpoint entry #{i+1} missing required 'name' string field.")
                    sys.exit(1)
                if 'url' not in endpoint or not isinstance(endpoint['url'], str):
                    logger.error(f"Endpoint entry #{i+1} missing required 'url' string field.")
                    sys.exit(1)
                    
            logger.debug(f"Configuration validation successful")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at '{file_path}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file '{file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred loading config: {e}")
        sys.exit(1)
import sys
from lib.config import load_config
from lib.monitor import monitor_endpoints
from lib.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Application starting")
    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        config = load_config(config_file)
        monitor_endpoints(config)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
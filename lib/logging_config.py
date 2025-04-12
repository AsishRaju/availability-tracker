import logging
import os

def setup_logging(log_dir="logs"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    root_logger.setLevel(logging.DEBUG)
    
    standard_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(pathname)s:%(lineno)d\n')
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(standard_formatter)
    
    normal_log = logging.FileHandler(os.path.join(log_dir, "monitor.log"))
    normal_log.setLevel(logging.INFO)
    normal_log.setFormatter(standard_formatter)
    
    error_log = logging.FileHandler(os.path.join(log_dir, "error.log"))
    error_log.setLevel(logging.ERROR)
    error_log.setFormatter(error_formatter)
    
    debug_log = logging.FileHandler(os.path.join(log_dir, "debug.log"))
    debug_log.setLevel(logging.DEBUG)
    debug_log.setFormatter(standard_formatter)
    
    root_logger.addHandler(console)
    root_logger.addHandler(normal_log)
    root_logger.addHandler(error_log)
    root_logger.addHandler(debug_log)
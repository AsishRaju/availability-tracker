import yaml
import sys

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            if not isinstance(config, list):
                print(f"Error: YAML content should be a list of endpoints. Found: {type(config)}")
                sys.exit(1)
            for i, endpoint in enumerate(config):
                if not isinstance(endpoint, dict):
                     print(f"Error: Endpoint entry #{i+1} is not a dictionary.")
                     sys.exit(1)
                if 'name' not in endpoint or not isinstance(endpoint['name'], str):
                    print(f"Error: Endpoint entry #{i+1} missing required 'name' string field.")
                    sys.exit(1)
                if 'url' not in endpoint or not isinstance(endpoint['url'], str):
                     print(f"Error: Endpoint entry #{i+1} missing required 'url' string field.")
                     sys.exit(1)
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{file_path}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred loading config: {e}")
        sys.exit(1)

load_config("sample.yaml")
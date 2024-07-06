import json
import re
from config.log_config import logger

def load_json_data(file_path):
    logger.info("Loading JSON data from file")
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            logger.info("JSON data loaded successfully")
            return data
    except Exception as e:
        logger.error(f"Error loading JSON data: {e}")
        raise

def read_env_file(file_path):
    logger.info("Reading the existing .env file")
    try:
        with open(file_path, 'r') as env_file:
            lines = env_file.readlines()
            logger.info(".env file read successfully")
            return lines
    except Exception as e:
        logger.error(f"Error reading .env file: {e}")
        raise

def create_env_dict(env_lines):
    logger.info("Creating a dictionary of existing .env variables")
    env_data = {}
    try:
        for line in env_lines:
            match = re.match(r'([^=]+)=(.*)', line.strip())
            if match:
                key, value = match.groups()
                env_data[key] = value
        logger.info("Dictionary of .env variables created successfully")
        return env_data
    except Exception as e:
        logger.error(f"Error creating dictionary of .env variables: {e}")
        raise

def update_env_data(env_data, new_data, key_mapping):
    logger.info("Updating the .env data with new values from JSON")
    try:
        for json_key, env_key in key_mapping.items():
            if json_key in new_data:
                env_data[env_key] = str(new_data[json_key])
        logger.info(".env data updated successfully")
    except Exception as e:
        logger.error(f"Error updating .env data: {e}")
        raise

def write_env_file(file_path, env_data):
    logger.info("Writing the updated .env data back to the file")
    try:
        with open(file_path, 'w') as env_file:
            for key, value in env_data.items():
                env_file.write(f'{key}={value}\n')
        logger.info("Successfully updated .env file with data from JSON")
    except Exception as e:
        logger.error(f"Error writing updated .env data to file: {e}")
        raise

def update_env():
    json_file_path = 'local_data.json'
    env_file_path = '.env'
    key_mapping = {
        "operator_id": "OPERATOR_ID",
        "zr_id": "ZR_ID"
    }

    new_data = load_json_data(json_file_path)
    env_lines = read_env_file(env_file_path)
    env_data = create_env_dict(env_lines)
    update_env_data(env_data, new_data, key_mapping)
    write_env_file(env_file_path, env_data)


import os
import re
import glob
import logging

#steamapps_path = r".\steamapps_test"
steamapps_path = r"C:\Program Files (x86)\Steam\steamapps"
config_file_path = r"C:\Program Files (x86)\Steam\user_language.cfg"
blacklist_file = "blacklist_appmanifest.cfg"
log_folder_path = r"C:\Users\user\boosteroid-experience\logs\language_games_logs"

if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

log_file_path = os.path.join(log_folder_path, "end.log")

logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"End.exe is launched. Version: 1.3")

def extract_user_language(filename):
    logging.info(f"Extracting user language from file: {filename}")
    with open(filename, 'r', encoding='utf-8', newline='\n') as file:
        data = file.read()

    user_config_match = re.search(r'"UserConfig"\s*{(.+?)\s*}', data, re.DOTALL)

    if user_config_match:
        user_config_block = user_config_match.group(1)

        language_match = re.search(r'"language"\s+"([^"]+)"', user_config_block)

        if language_match:
            user_language = language_match.group(1)
            logging.info(f"User language '{user_language}' extracted from UserConfig block.")
            return user_language
        else:
            logging.warning("Language not found in UserConfig block.")
            return None
    else:
        logging.warning("UserConfig block not found in the file.")
        return None

def write_user_language(user_language):
    with open(config_file_path, 'w', encoding='utf-8', newline='\n') as output_file:
        output_file.write(user_language)
        logging.info(f"User language '{user_language}' has been written to user_language.cfg.")

blacklist = set()
if os.path.exists(blacklist_file):
    with open(blacklist_file, 'r', encoding='utf-8', newline='\n') as blacklist_file:
        blacklist = {line.strip() for line in blacklist_file}

try:
    with open(config_file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
except FileNotFoundError:
    print(f"File '{config_file_path}' not found.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

for filename in glob.glob(os.path.join(steamapps_path, "appmanifest_*.acf")):
    if os.path.basename(filename) in blacklist:
        logging.info(f"File: {filename} is in the blacklist, skipping.")
        continue
    try:
        user_language = extract_user_language(filename)
    except FileNotFoundError:
        logging.warning(f"File not found: {filename}. Skipping.")
        continue

    if user_language and user_language.lower() != file_contents:
        write_user_language(user_language)
        logging.info(f"File: {filename}, User language is {user_language} writing to user_language.cfg.")
        break
    else:
        logging.info(f"File: {filename}, User language is {file_contents}, ignoring the writing to user_language.cfg.")
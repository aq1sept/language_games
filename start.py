import os
import re
import logging
import datetime

#folder_path = r".\steamapps_test"
folder_path = r"C:\Program Files (x86)\Steam\steamapps"
config_file_path = "user_language.cfg"
blacklist_file_path = "blacklist_appmanifest.cfg"
log_folder_path = r"C:\Users\user\boosteroid-experience\logs\language_games_logs"

if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

log_file_path = os.path.join(log_folder_path, "start.log")

logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def read_file_lines(file_path):
    with open(file_path, "r", encoding="utf-8", newline='\n') as file:
        return [line.strip() for line in file]

if not os.path.isfile(config_file_path):
    with open(config_file_path, "w", encoding="utf-8", newline='\n') as config_file:
        config_file.write("english")
    logger.info(f"Created {config_file_path} with default language 'english'.")

config_text = read_file_lines(config_file_path)[0]

blacklisted_filenames = set()
if os.path.isfile(blacklist_file_path):
    blacklisted_filenames = set(read_file_lines(blacklist_file_path))

for filename in os.listdir(folder_path):
    if filename.startswith("appmanifest_") and filename.endswith(".acf") and filename not in blacklisted_filenames:
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, "r+", encoding="utf-8", newline='\n') as manifest_file:
                manifest_lines = manifest_file.readlines()
                manifest_text = "".join(manifest_lines)

                manifest_text = re.sub(
                    r'("UserConfig"\s*{[\s\S]*?"language"\s*")(.+?)("\s*[\s\S]*?})',
                    fr'\1{config_text}\3',
                    manifest_text,
                    flags=re.DOTALL,
                )

                manifest_file.seek(0)
                manifest_file.write(manifest_text)
                manifest_file.truncate()

            logger.info(f"Updated language in file {filename}.")
        except FileNotFoundError:
            logger.warning(f"File {filename} not found. Skipping.")

import os
import re
import sys
import datetime

folder_path = "C:\\Program Files (x86)\\Steam\\steamapps"
config_file_path = "user_language.cfg"
log_file_path = "start_log.txt"

if not os.path.isfile(config_file_path):
    with open(config_file_path, "w") as config_file:
        config_file.write("english")

log_file = open(log_file_path, "a")

original_stdout = sys.stdout
sys.stdout = log_file

def log_with_timestamp(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)

with open(config_file_path, "r") as config_file:
    config_text = config_file.read().strip()

for filename in os.listdir(folder_path):
    if filename.startswith("appmanifest_") and filename.endswith(".acf"):
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, "r+") as manifest_file:
                manifest_text = manifest_file.read()

                manifest_text = re.sub(r'("UserConfig"\s*{[\s\S]*?"language"\s*")(.+?)("\s*[\s\S]*?})', fr'\1{config_text}\3', manifest_text, flags=re.DOTALL)

                manifest_file.seek(0)
                manifest_file.write(manifest_text)
                manifest_file.truncate()

            log_with_timestamp(f"File {filename} updated.")
        except FileNotFoundError:
            log_with_timestamp(f"File {filename} not found. Skipping.")

sys.stdout = original_stdout
log_file.close()
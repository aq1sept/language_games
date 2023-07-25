# VERSION: 2.2
import os
import re

#folder_path = r"C:\Users\admin\Desktop\git\language_games\steamapps_test"
folder_path = "C:\\Program Files (x86)\\Steam\\steamapps"
config_file_path = "user_language.cfg"
blacklist_file_path = "blacklist_appmanifest.cfg"

if not os.path.isfile(config_file_path):
    with open(config_file_path, "w", encoding="utf-8") as config_file:
        config_file.write("english")

with open(config_file_path, "r", encoding="utf-8") as config_file:
    config_text = config_file.read().strip()

blacklisted_filenames = set()
if os.path.isfile(blacklist_file_path):
    with open(blacklist_file_path, "r", encoding="utf-8") as blacklist_file:
        for line in blacklist_file:
            filename = line.strip()
            if filename:
                blacklisted_filenames.add(filename)

for filename in os.listdir(folder_path):
    if (
        filename.startswith("appmanifest_")
        and filename.endswith(".acf")
        and filename not in blacklisted_filenames
    ):
        file_path = os.path.join(folder_path, filename)

        try:
            with open(file_path, "r+", encoding="utf-8") as manifest_file:
                manifest_text = manifest_file.read()

                manifest_text = re.sub(
                    r'("UserConfig"\s*{[\s\S]*?"language"\s*")(.+?)("\s*[\s\S]*?})',
                    fr'\1{config_text}\3',
                    manifest_text,
                    flags=re.DOTALL,
                )

                manifest_file.seek(0)
                manifest_file.write(manifest_text)
                manifest_file.truncate()

            print(f"File {filename} updated.")
        except FileNotFoundError:
            print(f"File {filename} not found. Skipping.")
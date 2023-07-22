# VERSION: 2.2
import os
import re
import glob

def extract_user_language(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read()

    user_config_match = re.search(r'"UserConfig"\s*{(.+?)\s*}', data, re.DOTALL)

    if user_config_match:
        user_config_block = user_config_match.group(1)

        language_match = re.search(r'"language"\s+"([^"]+)"', user_config_block)

        if language_match:
            user_language = language_match.group(1)
            return user_language
        else:
            print("Language not found in UserConfig block.")
            return None
    else:
        print("UserConfig block not found in the file.")
        return None

steamapps_path = r"C:\Users\admin\Desktop\git\language_games\steamapps_test"
# steamapps_path = r"C:\Program Files (x86)\Steam\steamapps"
blacklist_file = "blacklist_appmanifest.cfg"

blacklist = []
if os.path.exists(blacklist_file):
    with open(blacklist_file, 'r', encoding='utf-8') as blacklist_file:
        blacklist = [line.strip() for line in blacklist_file]

english_found = False

for filename in glob.glob(os.path.join(steamapps_path, "appmanifest_*.acf")):
    if os.path.basename(filename) in blacklist:
        print(f"File: {filename} is in the blacklist, skipping.")
        continue

    user_language = extract_user_language(filename)

    if user_language and user_language.lower() != "english":
        with open("user_language.cfg", 'w', encoding='utf-8') as output_file:
            output_file.write(user_language)
            print(f"User language '{user_language}' has been written to user_language.cfg.")
            english_found = False
        break
    else:
        print(f"File: {filename}, User language is 'english', ignoring the writing to user_language.cfg.")
        english_found = True
    
if english_found:
    with open("user_language.cfg", 'w', encoding='utf-8') as output_file:
        output_file.write("english")
        print("User language 'english' has been written to user_language.cfg.")
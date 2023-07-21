import os
import re
import glob

def extract_user_language(filename):
    with open(filename, 'r') as file:
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

steamapps_path = r"C:\Program Files (x86)\Steam\steamapps"

for filename in glob.glob(os.path.join(steamapps_path, "appmanifest_*.acf")):
    user_language = extract_user_language(filename)

    if user_language and user_language.lower() != "english":
        with open("user_language.cfg", 'w') as output_file:
            output_file.write(user_language)
            print(f"User language '{user_language}' has been written to user_language.cfg.")
        break
    else:
        print(f"File: {filename}, User language is 'english', ignoring the writing to user_language.cfg.")

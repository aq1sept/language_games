import re

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

if __name__ == "__main__":
    filename = "appmanifest_10.acf"
    user_language = extract_user_language(filename)
    
    if user_language and user_language.lower() != "english":
        with open("user_language.cfg", 'w') as output_file:
            output_file.write(user_language)
            print(f"User language '{user_language}' has been written to user_language.cfg.")
    else:
        print("User language is 'english', ignoring the writing to user_language.cfg.")

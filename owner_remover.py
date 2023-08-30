import re
import os

directory_path = r"C:\Program Files (x86)\Steam\steamapps"

file_list = [f for f in os.listdir(directory_path) if f.startswith("appmanifest_") and f.endswith(".acf")]

pattern = re.compile(r'("LastOwner"\s+")\d+"')

for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        continue

    new_content = pattern.sub(r'\1"', content)

    with open(file_path, 'w') as file:
        file.write(new_content)

print("Завершено.")

import re
import os

# Путь к директории, содержащей файлы appmanifest_*.acf
directory_path = r".\steamapps_test"

# Получаем список файлов с именами, соответствующими шаблону appmanifest_*.acf
file_list = [f for f in os.listdir(directory_path) if f.startswith("appmanifest_") and f.endswith(".acf")]

# Регулярное выражение для замены цифр в строке "LastOwner" на пустоту
pattern = re.compile(r'("LastOwner"\s+")\d+"')

# Обход каждого файла в списке
for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    
    # Открываем файл для чтения и чтения всех строк
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Заменяем цифры в строке "LastOwner" на пустоту
    new_content = pattern.sub(r'\1"', content)
        
    # Записываем новое содержимое обратно в файл
    with open(file_path, 'w') as file:
        file.write(new_content)

print("Завершено.")

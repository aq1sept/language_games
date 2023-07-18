import os
import datetime

# Путь к папке, содержащей файлы appmanifest_*.acf
manifest_folder = "C:\\Program Files (x86)\\Steam\\steamapps"

# Путь к файлу лога
log_file = "end_log.txt"

# Открытие файла лога в режиме добавления (append)
with open(log_file, "a") as log:
    # Запись отметки времени в файл лога
    log.write(f"--- Log started: {datetime.datetime.now()} ---\n")

    # Перебор файлов в папке
    for file_name in os.listdir(manifest_folder):
        if file_name.startswith("appmanifest_") and file_name.endswith(".acf"):
            file_path = os.path.join(manifest_folder, file_name)

            try:
                # Чтение содержимого файла
                with open(file_path, "r") as file:
                    manifest_lines = file.readlines()

                # Поиск и изменение значения language в блоке UserConfig
                updated_lines = []
                for line in manifest_lines:
                    if line.strip().startswith("\"language\""):
                        line = line.split("\"")[3]  # Получаем значение после второй кавычки
                        if line.lower() != "english":
                            updated_lines.append(line)
                        break  # Прерываем цикл после нахождения первого значения "language"

                # Запись значения language в файл config.txt
                if updated_lines:
                    with open("config.txt", "w") as config_file:
                        config_file.write(updated_lines[0])

            except FileNotFoundError as e:
                # Запись информации об ошибке в файл лога
                log.write(f"File not found: {file_path}\n")

    # Запись отметки времени окончания в файл лога
    log.write(f"--- Log ended: {datetime.datetime.now()} ---\n")

import os
import datetime

manifest_folder = "C:\\Program Files (x86)\\Steam\\steamapps"
log_file = "end_log.txt"

with open(log_file, "a") as log:
    log.write(f"--- Log started: {datetime.datetime.now()} ---\n")

    for file_name in os.listdir(manifest_folder):
        if file_name.startswith("appmanifest_") and file_name.endswith(".acf"):
            file_path = os.path.join(manifest_folder, file_name)

            try:
                with open(file_path, "r") as file:
                    manifest_lines = file.readlines()

                updated_lines = []
                for line in manifest_lines:
                    if line.strip().startswith("\"language\""):
                        line = line.split("\"")[3]
                        if line.lower() != "english":
                            updated_lines.append(line)
                        break

                if updated_lines:
                    with open("user_language.cfg", "w") as config_file:
                        config_file.write(updated_lines[0])

            except FileNotFoundError as e:
                log.write(f"File not found: {file_path}\n")

    log.write(f"--- Log ended: {datetime.datetime.now()} ---\n")

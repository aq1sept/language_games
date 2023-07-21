from os import listdir
from os.path import isfile, join

path = "G:\SteamLibrary\steamapps\\" # Sets the path for thing. Copy-Paste your steam library steamapps folder here.


files = [f for f in listdir(path) if isfile(join(path, f))] # Gets only files within the steamapps folder.

for f in files:
    # Open Files and read lines
    selected_file = path + f
    current_open_file = open(selected_file)
    file_content = current_open_file.readlines()

    # Store file Information
    file_name = '       "file name"' + "     " + selected_file + '\n'
    name_of_game = file_content[5]
    buildID = file_content[11]

    print(name_of_game, buildID)
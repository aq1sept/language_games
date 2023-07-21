import json

# Read the content of the .acf file
with open("steam_appid.acf", "r") as f:
    data = json.load(f)

# Change the value of the "Name" key
data["Name"] = "New Name"

# Write the changed content back to the file
with open("steam_appid.acf", "w") as f:
    json.dump(data, f, indent=4)

import json

with open ("content.json", "r") as file:
    content = json.load(file)

print(content["sections"][0]["activitySubtitle"])

x = [
    {"Name": "Correct"},
    {"Name": "Incorrect"}
]

matches = [item for item in x if item["Name"] == "Correct"][0]
print(matches)

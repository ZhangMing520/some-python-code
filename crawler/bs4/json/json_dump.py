import json

listStr = [
    {"city": "西雅图"}, {"name": "jerry"}
]

# Object of type 'set' is not JSON serializable
json.dump(listStr, open("listStr.json", "w", encoding="utf8"), ensure_ascii=False)

import json
import chardet

listStr = [1, 2, 3]
tupleStr = (1, 2, 3)

dictStr = {
    "city": "北京",
    "name": "tom"
}

print(json.dumps(listStr))
print(json.dumps(tupleStr))

print(json.dumps(dictStr, ensure_ascii=False))

# chardet.detect()  confidence 是检查精度
print(chardet.detect(bytes(json.dumps(dictStr), "utf8")))
print(chardet.detect(bytes(json.dumps(dictStr,ensure_ascii=False), "utf8")))

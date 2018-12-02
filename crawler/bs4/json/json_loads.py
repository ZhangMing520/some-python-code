import json

strList = '[1,2,3,4]'

# 最后不能有 ,
strDict = '''{
    "city": "北京",
    "name": "tom"
}'''

print(json.loads(strDict))
print(json.loads(strList))

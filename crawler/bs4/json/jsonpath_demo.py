"""
    https://www.lagou.com/lbs/getAllCitySearchLabels.json
"""

from urllib import request
import jsonpath
import json
import chardet

url = "https://www.lagou.com/lbs/getAllCitySearchLabels.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36 "
    
}

# headers=headers 否则参数会传递错误
req = request.Request(url, headers=headers)
resp = request.urlopen(req)
html = resp.read()

json_obj = json.loads(html)

city_list = jsonpath.jsonpath(json_obj, "$..name")

print(city_list)
print(type(city_list))

json.dump(city_list, open("city.json", "w", encoding="utf8"), ensure_ascii=False)

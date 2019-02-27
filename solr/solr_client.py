from urllib import request
import json
import requests

# http://192.168.15.13:29999/solr/index.html#/ahkjt-core/query
select_url = "http://192.168.15.13:29999/solr/ahkjt-core/select?q=*:*&wt=json"
resp = request.urlopen(select_url)

#
html = resp.read().decode("utf8")
html_json = json.loads(html, encoding="utf8")
docs = html_json['response']['docs']

# http://192.168.15.13:29999/solr/ahkjt-core/update?_=1543845018820&boost=1.0&commitWithin=1000&overwrite=true&wt=json
update_url = "http://192.168.15.13:29999/solr/ahkjt-core/update?wt=json&indent=on"

# 需要有提交参数
update_params = {
    "boost": 1.0,
    "commitWithin": 1000,
    "overwrite": "true",
}

for doc in docs:
    # id+ 97重新提交 删除version
    doc["id"] = doc["id"] + 97
    del doc["_version_"]

    # add 需要知道是什么操作
    data = {"add": {"doc": doc}}

    print(data)

    r = requests.post(update_url, json=data, params=update_params)
    print(r.text)

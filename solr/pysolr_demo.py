"""
    使用第三方 solr 库

    pip install pysolr
"""
import pysolr

solr = pysolr.Solr("http://192.168.15.13:8091/solr/solr_cores_high_new_tech/")

params = {
    "rows": 10000,
    "indent": "on",
    "wt": "json",
    "fl": "pubId, zhTitle, cabstract",
}
results = solr.search(q="type:2", **params)

for r in results:
    print(r)

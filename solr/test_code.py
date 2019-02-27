import requests

solr_select_url = "http://192.168.15.13:8091/solr/solr_cores_high_new_tech/select?"
params = {
    "indent": "on",
    "wt": "json",
    "q": "type:2",
    "fl": "pubId",
}

resp = requests.get(solr_select_url, params)
print(resp.json()['response']['numFound'])



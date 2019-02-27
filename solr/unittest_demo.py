import unittest
import requests
import pysolr
import warnings


class TestDemo(unittest.TestCase):
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def requests_solr(self):
        """
         pysolr 速度
        :return:
        """
        params = {
            "rows": 10000,
            "indent": "on",
            "wt": "json",
            "q": "type:2",
            "fl": "pubId, zhTitle, cabstract",
        }

        solr_select_url = "http://192.168.15.13:8091/solr/solr_cores_high_new_tech/select?"
        resp = requests.get(solr_select_url, params)
        docs = resp.json()['response']['docs']
        return docs

    def test_pysolr(self):
        solr = pysolr.Solr("http://192.168.15.13:8091/solr/solr_cores_high_new_tech/")

        params = {
            "rows": 10000,
            "indent": "on",
            "wt": "json",
            "fl": "pubId, zhTitle, cabstract",
        }
        warnings.simplefilter("ignore", ResourceWarning)
        results = solr.search(q="type:2", **params)

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass


if __name__ == '__main__':
    unittest.main()

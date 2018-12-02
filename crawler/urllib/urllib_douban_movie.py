"""
    豆瓣电影
    
    https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=20&limit=20
"""

import urllib.request as request
import urllib.parse as parse

BASE_URL = "https://movie.douban.com/j/chart/top_list"

headers = {
    # "Connection": "keep-alive",
    # "Accept": "*/*",
    # "X-Requested-With": "XMLHttpRequest",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
}


def main():
    form_data = {
        "type": "11",
        "interval_id": "100:90",
        "action": " ",
        "start": "0",
        "limit": "20",
    }
    
    data_encode = parse.urlencode(form_data)
    req = request.Request(BASE_URL, data=str.encode(data_encode), headers=headers)
    resp = request.urlopen(req)
    html = resp.read().decode("utf8")
    print(html)


if __name__ == "__main__":
    main()

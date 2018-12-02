"""
获取贴吧页面

https://tieba.baidu.com/f?ie=utf-8&kw=%E6%9D%8E%E6%AF%85&pn=50
"""

import urllib.request as request
import urllib.parse as parse

BASE_URL = "https://tieba.baidu.com/f"
PAGE_SIZE = 50

HEADERS = {
    # "Host": "www.baidu.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
}


def prompt_msg():
    """
     一些提示信息
    """
    kw = input("请输入你需要爬取的贴吧名城:")
    begin_page = int(input("请输入起始页:"))
    end_page = int(input("请输入结束页:"))
    
    kw_params = {"kw": kw}
    url_prefix = BASE_URL + "?" + parse.urlencode(kw_params)
    
    for page in range(begin_page, end_page + 1):
        html = load_page(url_prefix, page)
        handle_html(html)


def load_page(url_prefix, page):
    """
        抓取页面
    """
    full_url = url_prefix + "&pn=" + str((page - 1) * PAGE_SIZE)
    print("html url:%s" % full_url)
    req = request.Request(url=full_url, headers=HEADERS)
    
    resp = request.urlopen(req)
    return resp.read().decode("utf8")


def handle_html(html):
    """
        处理页面内容
    """
    print(html)


def main():
    prompt_msg()


if __name__ == "__main__":
    main()

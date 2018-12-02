"""
    获取 https 内容
    
    https://www.12306.cn/index/
    好像不需要 ssl 也可以访问 ，加了还不能访问了
"""

import urllib.request as request
import ssl

# 忽略未经核实的ssl证书
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.12306.cn/index/"

req = request.Request(url)

resp = request.urlopen(req)

html = resp.read().decode("utf8")

print(html)

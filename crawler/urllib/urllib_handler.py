"""
 urllib2 在python3中被修改为 urllib.request
"""

import urllib.request
import urllib.parse

headers = {
    # "Host": "www.baidu.com",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
}

# url转码参数
decode_param = urllib.parse.urlencode({"wd": "机器学习"})

# url 解码
param = urllib.parse.unquote(decode_param)

# 最后一个 / 不能少
url = "http://www.baidu.com/"
# Request 构造请求对象
req = urllib.request.Request(url=url, headers=headers)

# 向指定的url地址发送请求，并返回服务器响应的类文件对象
resp = urllib.request.urlopen(req)

# 服务器返回的类文件对象支持python文件对象的操作方法
# read()方法就是读取文件里的全部内容，返回是字节
html = resp.read().decode("utf8")

print(html)

# 返回http的响应吗
print(resp.getcode())

# 返回实际数据的真实url，防止重定向问题
print(resp.geturl())

# 返回 服务器响应的响应头
print(resp.info())

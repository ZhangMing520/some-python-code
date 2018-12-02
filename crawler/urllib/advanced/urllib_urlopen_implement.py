"""
    自定义handler实现urlopen
    
    HTTPHandler() -> handler -> build_opener(handler) -> opener -> open(req)
"""

import urllib.request as request

# 构建一个 HTTPHandler 对象 ，支持处理http请求
# debuglevel=1 自动打开debug log 模式，会打印收发包信息
http_handler = request.HTTPHandler(debuglevel=1)

# 调用 build_opener() 方法构建自定义的 opener对象，参数是 handler对象
opener = request.build_opener(http_handler)

req = request.Request("http://www.baidu.com/")

resp = opener.open(req)

print(resp.read().decode("utf8"))

"""
 使用代理访问网站
 
 代理ip网站;
 [西刺]（http://www.xicidaili.com/nt/）
 [快代理免费代理]
 [Proxy360代理]
 [全网代理ip]
"""

from urllib import request
import os

# 可以将用户名或者密码写到环境变量中，获取而不暴露
proxy_user = os.environ.get("proxy_user")

proxySwitch = True

# 字典类型参数  指定 代理类型 {"http/ https":"ip:port"}
# 如果代理需要授权  {"http":"账号:密码@ip:port"}
http_proxy_handler = request.ProxyHandler({"http": "221.204.119.175:9797"})

null_proxy_handler = request.ProxyHandler({})

if proxySwitch:
    opener = request.build_opener(http_proxy_handler)
else:
    opener = request.build_opener(null_proxy_handler)

# 构建一个全局的 opener 之后所有的请求都可以使用 urlopen() 方式打开 并且附带 handler 功能
request.install_opener(opener)

req = request.Request("http://www.baidu.com/")

resp = request.urlopen(req)

print(resp.read().decode("utf8"))

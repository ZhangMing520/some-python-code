"""
    代码实现代理用户密码认证
    
    urllib_proxy_handler.py 中有简单办法
    
    ProxyBasicAuthHandler : 代理用户密码验证
    HTTPBasicAuthHandler ： web端用户密码验证
"""

from urllib import request

user = "proxy_user"
password = "proxy_password"

proxy_server = "221.204.119.175:9797"

# 构建一个密码管理对象，用来保存需要处理的用户名和密码
password_mgr = request.HTTPPasswordMgrWithDefaultRealm()

# 添加账户信息 第一个参数realm与远程服务器相关的域信息，一般不用管
password_mgr.add_password(None, proxy_server, user, password)

# 构建一个代理基础用户名和密码验证的handler对象
proxyauth_handler = request.ProxyBasicAuthHandler(password_mgr=password_mgr)

opener = request.build_opener(proxyauth_handler)

req = request.Request("http://www.baidu.com/")

print(opener.open(req).read().decode("utf8"))

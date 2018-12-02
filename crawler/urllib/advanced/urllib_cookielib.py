"""
    cookielib
    
    第一次 post 获取cookie，后面都会携带此 cookie
    
    后面就可以使用此 cookie 访问其他网页
"""

from urllib import request, parse
from http import cookiejar

# cookie
cookie = cookiejar.CookieJar()

#  handler
cookie_handler = request.HTTPCookieProcessor(cookiejar=cookie)

opener = request.build_opener(cookie_handler)

opener.addheaders = [
    ("User-Agent",
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36")
]

data = {
    "email": "",
    "password": "",
}

data_encode = parse.urlencode(data)

url = "http://www.renren.com/PLogin.do"
req = request.Request(url, data=str.encode(data_encode))

resp = opener.open(req)
print(resp.read().decode("utf8"))

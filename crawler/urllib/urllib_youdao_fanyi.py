"""
    有道翻译
    req:
    POST http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule HTTP/1.1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36
    i=%E4%BD%A0%E5%A5%BD&from=AUTO&to=AUTO&smartresult=dict&client=fanyideskweb&salt=1543132459693&sign=719df4ca25d4196b3b69d5f09c8b0d11&doctype=json&version=2.1&keyfrom=fanyi.web&action=FY_BY_REALTIME&typoResult=false
    
    resp:
    {"translateResult":[[{"tgt":"hello","src":"你好"}]],"errorCode":0,"type":"zh-CHS2en"}
    
    salt, sign 需要参考youdao_fanyi.js 获取
    
    参考此文章 http://www.tendcode.com/article/youdao-spider/
"""

import hashlib
import random
import time
import urllib.parse as parse
import urllib.request as request


def get_salt(e):
    """
        根据当前时间戳获取salt参数
    """
    t = str(int(time.time() * 1000) + random.randint(0, 10))
    
    value = "fanyideskweb" + e + t + "sr_3(QOHT)L2dx#uuGR@r"
    m = hashlib.md5()
    m.update(value.encode("utf8"))
    
    return {
        "salt": t,
        "sign": m.hexdigest()
    }


BASE_URL = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

wd = input("请输入需要翻译的内容：")

salt_sign_dict = get_salt(wd)

form_data = {
    "i": wd,
    "from": "AUTO",
    "to": "AUTO",
    "smartresult": "dict",
    "client": "fanyideskweb",
    "salt": salt_sign_dict["salt"],
    "sign": salt_sign_dict["sign"],
    "doctype": "json",
    "version": "2.1",
    "keyfrom": "fanyi.web",
    # "action": "FY_BY_REALTIME",
    "action": "FY_BY_CL1CKBUTTON",
    # "typoResult": "false"
    "typoResult": "true"
}

# Cookie 必须设置 OUTFOX_SEARCH_USER_ID
headers = {
    # 'Host': 'fanyi.youdao.com',
    # 'Origin': 'http://fanyi.youdao.com',
    # "Connection": "keep-alive",
    # "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    # "X-Requested-With": "XMLHttpRequest",
    # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # "Accept": "application/json, text/javascript, */*; q=0.01",
    
    'Cookie': 'OUTFOX_SEARCH_USER_ID=-1087941570@115.192.220.138;',
    'Referer': 'http://fanyi.youdao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:51.0) Gecko/20100101 Firefox/51.0',
    
}

# url 编码
data_encode = parse.urlencode(form_data)
# data 需要是bytes , data 有值就是post
req = request.Request(BASE_URL, data=str.encode(data_encode), headers=headers)
resp = request.urlopen(req)
html = resp.read().decode("utf8")
print(html)

"""
    登录知乎（现在不适用，_xsrf放在cookie中），需要 _xsrf，
"""

from bs4 import BeautifulSoup
import requests


def zhihu_login():
    # 构建一个 session对象 ，可以保存 cookie
    session = requests.Session()
    
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 "
            "Safari/537.36 "
    }
    
    # 获取登录页面，找到需要的post数据（_xsrf），同时记录当前网页的cookie值
    login_url = "https://www.zhihu.com/signup?next=%2F"
    session.get(login_url, headers=headers)
    
    # 这是之前的获取方法 此时 _xsrf 在页面上
    # html = session.get(login_url, headers=headers).text
    # bs = BeautifulSoup(html, features="lxml")
    # _xsrf = bs.find("input", attrs={"name": "_xsrf"}).get("value")
    
    real_login_url = "https://www.zhihu.com/api/v3/oauth/sign_in"
    data = {
    
    }





if __name__ == '__main__':
    zhihu_login()

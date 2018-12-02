"""
    https://www.qiushibaike.com/8hr/page/2/
    
    糗事百科
"""
from urllib import request
from lxml import etree
import json

url = "https://www.qiushibaike.com/8hr/page/1/"

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 "
        "Safari/537.36 "
}

req = request.Request(url=url, headers=headers)
resp = request.urlopen(req)
html = resp.read().decode("utf8")
print(html)

html_dom = etree.HTML(html)

duanzi_xpath = '//div[contains(@id,"qiushi_tag")]'
duanzi_list = html_dom.xpath(duanzi_xpath)
for ele in duanzi_list:
    username = ele.xpath('./div[@class="author clearfix"]//h2')[0].text
    image = ele.xpath('./div[@class="thumb"]//@src')
    content = ele.xpath('./a/div[@class="content"]/span')[0].text
    comment = ele.xpath('./div[@class="stats"]/span[@class="stats-comments"]//i')[0].text
    zan = ele.xpath('./div[@class="stats"]/span[@class="stats-vote"]//i')[0].text
    
    data = {
        "username": username,
        "image": image,
        "content": content,
        "comment": comment,
        "zan": zan,
    }
    
    dataStr = json.dumps(data, ensure_ascii=False)
    
    with open("duanzi.json", "a", encoding="utf8") as f:
        f.write(dataStr + "\n")

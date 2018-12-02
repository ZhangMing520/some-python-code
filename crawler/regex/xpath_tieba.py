"""
    利用 xpath 下载图片
    
    url:
    http://tieba.baidu.com/f?kw=%E7%BE%8E%E5%A5%B3&ie=utf-8&pn=50
    
    步骤：
    1. 获取每一个帖子的url
    2. 获取帖子中图片链接
    3. 下载图片
    
    
    decode("utf8", "ignore") 不是严格模式
"""

from urllib import request, parse
from lxml import etree

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}

BASE_URL = "http://tieba.baidu.com/f?"

TIE_ZI_BASE_URL = "https://tieba.baidu.com"

PAGE_SIZE = 50


class TiebaSpider(object):
    
    def __init__(self, kw, begin, end):
        self.kw = kw
        self.begin = begin
        self.end = end
    
    def get_tiezi_link(self):
        """
            获取贴吧中开始页和结束页
        :return:
        """
        
        for page in range(self.begin, self.end + 1):
            data = {
                "kw": self.kw,
                "pn": (page - 1) * PAGE_SIZE
            }
            
            full_url = BASE_URL + parse.urlencode(data)
            req = request.Request(url=full_url, headers=headers)
            html = request.urlopen(req).read().decode("utf8")
            
            # 百度将内容隐藏了
            content = etree.HTML(html.replace('<!--', '').replace('-->', ''))
            # tiezi_link_list = content.xpath('//div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit"]/@href')
            tiezi_link_list = content.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
            
            for link in tiezi_link_list:
                self.get_tiezi_image_link(link)
    
    def get_tiezi_image_link(self, tiezi_link):
        full_url = TIE_ZI_BASE_URL + tiezi_link
        req = request.Request(url=full_url, headers=headers)
        html = request.urlopen(req).read().decode("utf8", "ignore")
        
        content = etree.HTML(html)
        tiezi_image_link_list = content.xpath('//img[@class="BDE_Image"]/@src')
        
        for link in tiezi_image_link_list:
            self.handle_image_link(link)
    
    def handle_image_link(self, image_link):
        file_name = image_link[-10:]
        
        # wb  二进制
        with open("./images/" + file_name, 'wb') as f:
            req = request.Request(url=image_link, headers=headers)
            f.write(request.urlopen(req).read())
    
    def start(self):
        self.get_tiezi_link()
        
        print("over")


def main():
    kw = input("请输入你需要爬取图片的贴吧：")
    begin = int(input("请输入开始页："))
    end = int(input("请输入结束页："))
    
    spider = TiebaSpider(kw, begin, end)
    spider.start()


if __name__ == "__main__":
    main()

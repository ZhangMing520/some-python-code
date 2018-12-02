"""
    此例子是将采集和解析分阶段，使用多线程，不是生产者消费者模式

    Queue.get(False) raise the Empty exception
"""
from threading import Thread
from queue import Queue, Empty
from lxml import etree
import requests
import json
import time

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 "
        "Safari/537.36 "
}


class CrawlerThread(Thread):
    def __init__(self, thread_name, page_queue):
        # 调用父类构造方法
        super(CrawlerThread, self).__init__()
        
        self.name = thread_name
        self.pageQueue = page_queue
    
    def run(self):
        # 开始爬取网页
        while not CRAWL_EXIT:
            try:
                page = self.pageQueue.get(False)
                url = "https://www.qiushibaike.com/8hr/page/" + str(page) + "/"
                html = requests.get(url, headers=headers).text
                dataQueue.put(html)
            except Empty as e:
                pass


class ParseThread(Thread):
    def __init__(self, thread_name):
        # 调用父类构造方法
        super(ParseThread, self).__init__()
        
        self.name = thread_name
    
    def run(self):
        while not PARSE_EXIT:
            try:
                html = dataQueue.get(False)
                self._parse(html)
            except Empty as e:
                pass
    
    def _parse(self, html):
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
            
            data_str = json.dumps(data, ensure_ascii=False)
            
            with open("multi_duanzi.json", "a", encoding="utf8") as f:
                f.write(data_str + "\n")


if __name__ == '__main__':
    pageQueue = Queue(maxsize=10)
    dataQueue = Queue()
    CRAWL_EXIT = False
    PARSE_EXIT = False
    
    for i in range(1, 3):
        pageQueue.put(i)
    
    crawlerNameList = ["采集线程1", "采集线程2", "采集线程3"]
    for threadName in crawlerNameList:
        thread = CrawlerThread(threadName, pageQueue)
        thread.start()
    
    parserNameList = ["解析线程1", "解析线程2", "解析线程3"]
    for threadName in parserNameList:
        thread = ParseThread(threadName)
        thread.start()
    
    # 线程同步还有问题 暂时没有找到好的解决办法
    # 主要是从 pageQueue 中 get 太快，请求数据需要时间 dataQueue 中还是空的
    while pageQueue.empty():
        time.sleep(4)
        
        if dataQueue.empty():
            CRAWL_EXIT = True
            PARSE_EXIT = True
            break

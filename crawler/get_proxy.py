"""
获取 https://www.xicidaili.com/ 代理

无忧代理ip

芝麻代理ip

西刺代理ip

云连代理ip

代理：
https://proxy.mimvp.com/free.php?proxy=in_hp
http://www.coobobo.com/free-http-proxy
http://ip.zdaye.com/
http://www.mayidaili.com/free/anonymous/%E9%AB%98%E5%8C%BF
http://http.taiyangruanjian.com/
http://http.zhimaruanjian.com/
http://ip.jiangxianli.com

66代理
云代理
快代理
西刺代理
无忧代理
免费IP代理
"""

import logging as log
import requests
from lxml import etree
from requests import exceptions
from multiprocessing import Pool, Queue
import threading

log.basicConfig(level=log.INFO, format='%(asctime)s - %(filename)s - %(name)s - '
                                       '%(lineno)s - %(levelname)s - %(message)s',
                # datefmt='%Y %a, %d %b %H:%M:%S',
                handlers={log.FileHandler(filename='get_proxy.log', mode='w', encoding='utf-8')})

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"

JSON_ACCEPT = "application/json, text/javascript, */*; q=0.01"
HTML_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"

HTML_COMMON_HEADERS = {
    "Accept": HTML_ACCEPT,
    "User-Agent": USER_AGENT,
}

TR_IP_INDEX = 1
TR_PORT_INDEX = 2
TR_PROTOCOL_INDEX = 5

TEST_URL = 'http://m.audio699.com/'
BASE_URL = 'https://www.xicidaili.com/nt/'

lock = threading.Lock()
L = []

# 跨线程
queue = Queue()


def thread_worker(proxy_list):
    # log.info("代理总数目：%d", len(proxy_list))
    filter_list = []
    for ip_port in proxy_list:
        proxies = {
            'http': ip_port,
            'https': ip_port
        }
        delete_flag = False
        try:
            proxy_r = requests.get(TEST_URL, headers=HTML_COMMON_HEADERS, proxies=proxies, timeout=30)
            if proxy_r.status_code != 200:
                delete_flag = True
            else:
                global queue
                queue.put(ip_port)

                # lock.acquire()
                # try:
                #     global L
                #     L.append(ip_port)
                # finally:
                #     lock.release()

        except exceptions.RequestException as ex:
            # log.error("%s 请求异常", ip_port, exc_info=ex)
            delete_flag = True

        if delete_flag:
            # log.info("%s 无效IP，端口", ip_port)
            filter_list.append(ip_port)

    log.info("代理过滤后数目：%d", len(proxy_list) - len(filter_list))


def process_worker(page):
    http_proxy_list = []
    https_proxy_list = []
    socks_proxy_list = []

    home_url = BASE_URL + str(page)
    home_r = requests.get(home_url, headers=HTML_COMMON_HEADERS)
    log.info("【%s】 响应码：【%s】", home_url, home_r.status_code)

    html = etree.HTML(home_r.content.decode())
    for tr in html.xpath("//table[@id='ip_list']//td[@class='country']/.."):
        td = tr.xpath('td')
        scheme = td[TR_PROTOCOL_INDEX].text.lower()
        proxy = ''.join([scheme, '://', td[TR_IP_INDEX].text, ':', td[TR_PORT_INDEX].text])
        if scheme == 'https':
            http_proxy_list.append(proxy)
        elif scheme == 'http':
            https_proxy_list.append(proxy)
        elif scheme.startswith('socks'):
            socks_proxy_list.append('socks5' + proxy[proxy.index(':'):])

    total_list = [http_proxy_list, https_proxy_list, socks_proxy_list]
    threads = []
    for proxy_list in total_list:
        t = threading.Thread(target=thread_worker, args=(proxy_list,))
        t.start()
        threads.append(t)

    # 等待线程完成
    for t in threads:
        t.join()

    log.info("page【%d】代理获取完成", page)


def main():
    start_page = 1
    end_page = 20
    pool = Pool(end_page - start_page + 1)
    for page in range(start_page, end_page):
        pool.apply_async(process_worker, (page,))

    pool.close()
    pool.join()
    log.info("地址：【%s】，获取代理完成", BASE_URL)

    # if len(L) > 0:
    #     with open('proxy.txt', 'w') as file:
    #         for ip_host in L:
    #             file.write(ip_host + '\n')
    if queue.qsize() > 0:
        with open('proxy.txt', 'w') as file:
            while not queue.empty():
                file.write(queue.get() + '\n')

    log.info("地址：【%s】，写入代理完成", BASE_URL)


if __name__ == '__main__':
    main()

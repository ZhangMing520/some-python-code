import requests
import logging as log
from lxml import etree
import os
import time

log.basicConfig(level=log.INFO, format='%(asctime)s - %(filename)s - %(name)s - '
                                       '%(lineno)s - %(levelname)s - %(message)s',
                # datefmt='%Y %a, %d %b %H:%M:%S',
                handlers={log.FileHandler(filename='audio699_download.log', mode='a', encoding='utf-8')})

# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
PHONE_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"

JSON_ACCEPT = "application/json, text/javascript, */*; q=0.01"
HTML_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"

HTML_COMMON_HEADERS = {
    "Accept": HTML_ACCEPT,
    "User-Agent": PHONE_USER_AGENT,
}

SEARCH_URL = 'http://www.audio699.com/search'
PHONE_SEARCH_URL = 'http://m.audio699.com/search'


def search_book(keyword):
    """
    根据关键字获取电子书列表
    :param keyword:  关键字
    :return:
    """
    payload = {
        'keyword': keyword
    }
    search_r = requests.get(PHONE_SEARCH_URL, params=payload, headers=HTML_COMMON_HEADERS)
    log.info("搜索关键字【%s】相关电子书，响应码【%s】", keyword, search_r.status_code)
    html = etree.HTML(search_r.content.decode())

    title_href_dict_list = []
    for a in html.xpath('//div[@class="category-list"]//div[@class="info"]/h4/a'):
        dict_attr = dict(a.attrib)
        # href = dict_attr['href']
        # title = dict_attr['title']
        title_href_dict_list.append(dict_attr)

    return title_href_dict_list


def chapter_list(chapter_list_url):
    """
    获取电子书章节列表
    :param chapter_list_url:
    :return:
    """

    chapter_list_r = requests.get(chapter_list_url, headers=HTML_COMMON_HEADERS)
    log.info("获取电子书章节列表，请求地址：【%s】，响应码:【%s】", chapter_list_url, chapter_list_r.status_code)

    chapter_num_href_dict_list = []
    html = etree.HTML(chapter_list_r.content.decode())
    for a in html.xpath("//div[@class='playlist']/div[@class='plist']//a"):
        chapter_num_href_dict = dict(a.attrib)
        chapter_num_href_dict['chapter_num'] = a.text
        chapter_num_href_dict_list.append(chapter_num_href_dict)

    return chapter_num_href_dict_list


def chapter_detail(chapter_detail_url):
    """
    某一章节详情
    :param chapter_detail_url:
    :return:
    """
    chapter_detail_r = requests.get(chapter_detail_url, headers=HTML_COMMON_HEADERS)
    log.info("获取电子书章节详情，请求地址：【%s】，响应码:【%s】", chapter_detail_url, chapter_detail_r.status_code)

    html = etree.HTML(chapter_detail_r.content.decode())
    source = html.xpath("//audio/source")
    if len(source):
        return dict(source[0].attrib)['src']
    else:
        pass


DOWNLOAD_HEADERS = {
    "Accept-Encoding": "identity;q=1, *;q=0",
    "chrome-proxy": "frfr",
    "Range": "bytes=0-",
    "User-Agent": PHONE_USER_AGENT,
}


def download_m4a(m4a_download_url, book_name='no_name', chapter_num='1', re_download=False):
    m4a_save_path = os.sep.join(['audio', book_name])
    if not os.path.exists(m4a_save_path):
        os.makedirs(m4a_save_path)

    file_suffix = m4a_download_url[m4a_download_url.rindex('.'):]
    m4a_save_file_path = m4a_save_path + os.sep + chapter_num + file_suffix

    # 1.没有下载过 2.设置了重新下载
    if (not os.path.exists(m4a_save_file_path)) or re_download:
        download_r = requests.get(m4a_download_url, headers=DOWNLOAD_HEADERS)
        log.info("下载电子书章节，请求地址：【%s】，响应码:【%s】", m4a_download_url, download_r.status_code)
        with open(m4a_save_file_path, 'wb') as m4a:
            m4a.write(download_r.content)

        log.info("电子书：【%s】 章节：【%s】 下载地址：【%s】 本地保存目录：【%s】", book_name, chapter_num,
                 m4a_download_url, os.path.abspath(m4a_save_file_path))
    else:
        log.info("电子书：【%s】 章节：【%s】 下载地址：【%s】 本地保存目录：【%s】，已经下载", book_name, chapter_num,
                 m4a_download_url, os.path.abspath(m4a_save_file_path))


def main():
    title_href_dict_list = search_book('带着仓库到大明')
    # title_href_dict_list = search_book('赘婿')
    for title_href_dict in title_href_dict_list:
        book_name = title_href_dict['title']

        log.info("电子书:【%s】 获取章节列表", book_name)
        chapter_num_href_dict_list = chapter_list(title_href_dict['href'])
        for chapter_num_href_dict in chapter_num_href_dict_list:
            chapter_num = chapter_num_href_dict['chapter_num']

            log.info("电子书:【%s】 获取章节【%s】详情", book_name, chapter_num)
            m4a_download_url = chapter_detail(chapter_num_href_dict['href'])

            download_start = time.time()
            log.info("电子书：【%s】 章节：【%s】 下载地址：【%s】 开始下载", book_name, chapter_num, m4a_download_url)
            download_m4a(m4a_download_url, book_name, chapter_num)
            log.info("电子书：【%s】 章节：【%s】 下载地址：【%s】 下载耗时：【%d】s", book_name, chapter_num, m4a_download_url,
                     time.time() - download_start)

        log.info("电子书:【%s】 下载完成", book_name)


if __name__ == '__main__':
    main()

"""
    lxml 库测试  本地有问题

"""
from lxml import etree


def main():
    with open('./tieba.html') as f:
        fr = f.read()
        print(fr)
        
        # html = etree.HTML(text)
        # for li in html.xpath('//li'):
        #     print(li)

main()

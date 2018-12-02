"""
    beautifulsoup4 测试
    
    速度：
     正则 > lxml > bs4
"""

from bs4 import BeautifulSoup
import re

html = """
<ul>
  <li><a href="security/index.html" class="page">Security Announcements</a></li>
  <li><a href="guide/index.html" class="page">Getting Started Guide</a></li>
  <li><a href="general/index.html" class="page">General Concepts</a></li>
  <li><a href="index-actors.html" class="page">Actors</a></li>
  <li><a href="typed/index.html" class="page">Akka Typed</a></li>
  <li><a href="index-cluster.html" class="page">Clustering</a></li>
  <li><a href="stream/index.html" class="page">Streams</a></li>
  <li><a href="index-network.html" class="page">Networking</a></li>
  <ul>
"""

# 指定 lxml 解析
soup = BeautifulSoup(html, features="lxml")

# 打开本地 html 文件的方式创建对象
# soup = BeautifulSoup(open('index.html'))

# 格式化输出内容
# print(soup.prettify())


# soup.Tag  查找所有内容中第一个符合要求的标签
# print(soup.ul)
# print(soup.li)


# 标签 Tag 两个重要属性 name attrs
# soup 本身name 是[document] ，其他的都是标签本身名称
print(soup.name)
print(soup.ul.name)
print(soup.a.attrs)
print(soup.a['href'])

# string 标签内部的文字，当标签中只有唯一一个标签时候，string 也会返回最里面内容
print(soup.a.string)

# 列表显示子节点
print(soup.ul.contents)
print(soup.ul.children)

# 所有子孙节点
print(soup.ul.descendants)
for child in soup.ul.descendants:
    print(child)

# find_all(  name, attrs, text, limit, generator, **kwargs)
# name 参数可以查找所有名字为name的tag，字符串对象会被自动忽略掉

# 传入字符串 查找文档中的所有 <b> 标签 ，完整匹配
soup.find_all('b')
# 传入正则  <body> <b> ， 通过正则表达式 match() 来匹配
soup.find_all(re.compile("^b"))
# 传入列表  <a> <b>
soup.find_all(['a', 'b'])
# text 可以搜索文档中字符串内容 ， text 也可以是正则表达式，列表，字符串
soup.find_all(text="tom")
soup.find_all(text=re.compile(r"^tom"))

# css 选择器 , 类名加（.），id加（#） ， 返回类型是 list
soup.select("a")
# 组合查询
soup.select("p #link1")
# 属性查找，注意属性和标签中间不能有空格
soup.select("a[class='linkA']")

# get_text 获取内容
soup.select("title")[0].get_text()

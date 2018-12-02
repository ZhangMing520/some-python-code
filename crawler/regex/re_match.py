"""
    
    match 作用
    从头开始匹配一次就返回
    
    search 作用
    和 match 一样 ，从任意位置开始匹配一次就返回
    
    findall 作用：
    返回所有符合列表
    
    finditer 返回迭代器
    
    sub 替换
"""

import re

content = "hello Wrold python"
# re.I  忽略大小写
pattern = re.compile(r"([a-z]+) ([a-z]+)", re.I)
#  还可以指定开始和结束下标
m = pattern.match(content)

# 所有 group 之和
print(m.group(0))
# 第一个括号分组
print(m.group(1))
# 第二个括号分组
print(m.group(2))

# 对应上面下标
print(m.span(0))
print(m.span(1))
print(m.span(2))

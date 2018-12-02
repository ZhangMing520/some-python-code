"""
     UserWarning: Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead

    
    获取元素api：
    driver.find_element_by_id
    driver.find_element_by_name
    driver.find_element_by_xpath
    driver.find_element_by_link_text
    driver.find_element_by_partial_link_text
    driver.find_element_by_tag_name
    driver.find_element_by_class_name
    driver.find_element_by_css_selector
    driver.find_element(by=By.id, value="wrapper")
    
    内置等待条件：
    EC.title_is
    EC.title_contains
    EC.presence_of_element_located
    EC.visibility_of_element_located
    EC.visibility_of
    EC.presence_of_all_elements_located
    EC.text_to_be_present_in_element
    EC.text_to_be_present_in_element_value
    EC.frame_to_be_available_and_switch_to_it
    EC.invisibility_of_element_located
    EC.element_to_be_clickable
    EC.staleness_of
    EC.element_to_be_selected
    EC.element_located_to_be_selected
    EC.element_selection_state_to_be
    EC.element_located_selection_state_to_be
    EC.alert_is_present
    ...
"""

# 导入 webdriver
from selenium import webdriver
# 要想调用键盘按键操作需要引入 keys 包
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select

# 调用环境变量指定的 phantomJs 浏览器创建浏览器对象
# driver = webdriver.PhantomJS()

# 如果没有在环境变量中指定 phantomJs 位置
driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1\bin\phantomjs.exe")

# get 方法会一直等到页面被完全加载，然后程序才继续运行，通常测试会选择在这里 time.sleep(2)
driver.get("http://www.baidu.com/")

# 获取页面名为 wrapper 的id 标签的文本内容
data = driver.find_element_by_id("wrapper").text

driver.find_element(by=By.id, value="wrapper")

print(data)

print(driver.title)

# 生成当前页面快照并保存
driver.save_screenshot("baidu.png")

# 百度输入框
driver.find_element_by_id("kw").send_keys("长城")

# 模拟百度搜索按钮 click()
driver.find_element_by_id("su").click()

driver.save_screenshot("长城.png")

print(driver.page_source)

print(driver.get_cookies())

#  ctrl + a
driver.find_element_by_id("kw").send_keys(Keys.CONTROL, 'a')

# 回车
driver.find_element_by_id("su").send_keys(Keys.RETURN)

driver.find_element_by_id("kw").click()

# 当前 url
print(driver.current_url)

# 关闭当前页面 ，如果只有一个页面会关闭浏览器
driver.close()

# 关闭浏览器
driver.quit()

# select 标签
select = Select(driver.find_element_by_tag_name("select"))
# 索引从 0 开始
select.select_by_index(1)
# option value
select.select_by_value("0")
# option 文本值
select.select_by_visible_text("未审核")

# 全部取消选择
select.deselect_all()

# 处理弹窗提示或者获取提示信息
alert = driver.switch_to.alert()

# 切换窗口
driver.switch_to.window("this is window name")

# 通过 Windsow_handles 获取每个窗口对象
for handle in driver.window_handles:
    driver.switch_to.window(handle)

# 前进 后退
driver.forward()
driver.back()

# 删除 cookie
driver.delete_cookie("cookie name")

# 隐式等待是等待特定的时间 ， 显示等待是指定某一条件直到这个条件成立时继续执行
# ajax 异步加载数据

# 显示
# WebDriverWait 负责循环等待
from selenium.webdriver.support.ui import WebDriverWait

# expected_conditions 负责条件触发
from selenium.webdriver.support import expected_conditions as EC

try:
    # 页面一直循环，每 10s 判断一次 ， 直到 id="kw" 出现
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "kw")))

finally:
    driver.quit()

# 隐式
# wait 10s
driver.implicitly_wait(10)

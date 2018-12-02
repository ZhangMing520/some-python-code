from selenium import webdriver

import time

driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1\bin\phantomjs.exe")

driver.get("https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=")

#  向下滚动 10000像素
js = "document.body.scrollTop=10000"
time.sleep(3)

driver.save_screenshot("douban.png")

# 执行js语句
driver.execute_script(js)
time.sleep(10)

driver.save_screenshot("newdouban.png")

driver.quit()

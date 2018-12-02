from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1\bin\phantomjs.exe")
driver.get("https://www.douban.com/")
driver.save_screenshot("douban.png")

driver.find_element_by_name("form_email").send_keys("")
driver.find_element_by_name("form_password").send_keys("")
driver.find_element_by_id("captcha_field").send_keys("simple")

driver.find_element_by_class_name("bn-submit").click()

time.sleep(2)

driver.save_screenshot("douban.png")
with open("douban.html", "w", encoding="utf8") as f:
    f.write(driver.page_source)

driver.quit()

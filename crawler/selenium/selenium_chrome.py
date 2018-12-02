from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True

# 需要下载驱动
driver = webdriver.Chrome(executable_path=r"d:\chromedriver.exe", chrome_options=chrome_options)

import unittest

from selenium import webdriver
from bs4 import BeautifulSoup


class Douyu(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1\bin\phantomjs.exe")
    
    def testDouyu(self):
        self.driver.get("https://www.douyu.com/directory/all")
        while True:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, features="lxml")
            
            # 房间名  class ="ellipsis"
            rooms = soup.find_all(name="h3", attrs={"class": "ellipsis"})
            # 观看人数 class="dy-num fr"
            watchers = soup.find_all(name="span", attrs={"class": "dy-num fr"})
            
            for room, watcher in zip(rooms, watchers):
                print("观看人数：" + watcher.get_text().strip() + "\t房间名：" + room.get_text().strip())
            
            # shark-pager-next shark-pager-disable shark-pager-disable-next
            # str find
            if page_source.find("shark-pager-disable-next") != -1:
                # 最后一页
                break
            
            self.driver.find_element_by_class_name("shark-pager-next").click()
    
    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

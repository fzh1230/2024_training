from Common.basePage import BasePage
from selenium.webdriver.common.by import By
from time import sleep

class BaiduIndex(BasePage):

    baidu_index_url = "https://www.baidu.com"
    search_input = (By.ID, "kw")
    search_button = (By.ID, "su")

    def search_key(self, search_key):
        self.logger.info("开始搜索")
        self.wait_eleVisible(self.search_input, model='搜索框')
        self.clean_inputText(self.search_input, model='搜索框')
        self.input_text(self.search_input, text=search_key, model='搜索框')
        self.wait_eleVisible(self.search_button, model='"百度一下"搜索按钮')
        self.click_element(self.search_button, model='"百度一下"搜索按钮')
        self.driver.implicitly_wait(10)
        sleep(3)

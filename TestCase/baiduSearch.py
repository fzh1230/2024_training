# -*- coding: utf-8 -*-
import os
import time
import pytest
import allure
import requests
from selenium import webdriver
from PageObject.baiduIndex import BaiduIndex


@pytest.fixture(scope="class")
def init(request):
    driver = webdriver.Chrome()
    baidu_index = BaiduIndex(driver)
    request.cls.driver = driver
    request.cls.baidu_index = baidu_index
    baidu_index.logger.info("WebDriver 启动中")
    driver.get(baidu_index.baidu_index_url)
    baidu_index.logger.info(f"目标链接: {baidu_index.baidu_index_url}")
    driver.maximize_window()
    driver.implicitly_wait(10)
    baidu_index.logger.info("WebDriver 启动完成")
    yield
    driver.quit()
    baidu_index.logger.info("WebDriver 成功退出")


def process_query(query):

    query = query[:100]
    query = query.replace("<", "").replace(">", "")
    return query[:20]


def search_api(query):
    base_url = "http://www.baidu.com/s"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
    params = {"wd": query, "fr": "search"}
    response = requests.get(base_url, params=params, headers=headers)
    return response


@allure.feature("百度搜索作业")
@pytest.mark.usefixtures("init")
class TestBaiduSearch:

    @allure.story("搜索关键字 - UI 测试")
    @pytest.mark.baidu_search
    @pytest.mark.parametrize("key_word, expected_result", [
        ("小米武汉总部", "小米武汉总部"),
        ("a" * 101, "a" * 20),
        ("test<search>", "testsearch"),
        ("<test>search", "testsearch"),
        ("<test>", "test"),
        # ("", ""),  # 空输入
        # (" " * 101, " " * 20),  # 超长空格输入
        # ("a" * 20 + "<" + "b" * 20 + ">", "a" * 20),  # 特殊字符在中间
        # ("<a" * 50 + ">", "a" * 20),  # 大量特殊字符
        # ("1234567890" * 10, "12345678901234567890"),  # 边界输入（正好100字符）
        # ("1234567890" * 10 + "1", "12345678901234567890"),  # 边界输入（101字符）
        # ("12345678901" * 9, "12345678901234567890"),  # 边界输入（99字符）
        # ("1234567890" * 2, "12345678901234567890"),  # 边界输入（正好20字符）
        # ("12345678" * 2 + "1", "12345678123456781"),  # 边界输入（正好19字符）
        # ("1234567890" * 2 + "1", "123456789012345678901"),  # 边界输入（正好21字符）
        # ("<script>alert('test');</script>", "scriptalert('test');script")  # HTML/JS输入
    ])
    def test_search_ui(self, key_word, expected_result):
        # 输入搜索关键字
        self.baidu_index.search_key(key_word)

        # 获取搜索输入框的内容
        search_input_value = self.driver.find_element(*self.baidu_index.search_input).get_attribute("value")

        # 验证搜索框中的内容是否符合预期（截取前20个字符，并去掉<和>）
        expected_search_value = key_word[:100].replace("<", "").replace(">", "")[:20]
        assert search_input_value == expected_search_value, f"期望 '{expected_search_value}', 实际得到 '{search_input_value}'"

        # 验证页面标题
        web_title = self.driver.title
        assert expected_result in web_title, f"期望 '{expected_result}' 实际得到 '{web_title}'"


    @allure.story("demo测试是否成功")
    @pytest.mark.test_demo
    def test_demo(self):
        assert 1 == 1


if __name__ == '__main__':
    now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
    cur_path = os.path.dirname(os.path.realpath(__file__))
    report_path = os.path.join(cur_path, f'Report\\{now_time}')
    pytest.main(["-s", "-m", "baidu_search or test_demo", "--alluredir", report_path])
    os.system(f"allure serve {report_path}")

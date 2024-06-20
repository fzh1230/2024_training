# -*- coding: utf-8 -*-
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from Utils.myLog import MyLog

class BasePage(object):

    def __init__(self, driver):
        self.logger = MyLog().getLog()
        self.driver = driver


    def wait_eleVisible(self, loc, timeout=30, poll_frequency=0.5, model=None):
        try:
            start = datetime.now()
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.visibility_of_element_located(loc))
            end = datetime.now()
            self.logger.info(f'执行"{model}"时长:{end - start}')
        except TimeoutException:
            self.logger.exception(f'执行"{model}"失败')
            raise


    def find_element(self, loc, model=None):
        self.logger.info(f'开始查找"{model}"')
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            self.logger.exception(f'查找"{model}"失败')

            raise


    def find_elements(self, loc, model=None):
        self.logger.info(f'开始查找"{model}"')
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException:
            self.logger.exception(f'查找"{model}"失败')

            raise


    def input_text(self, loc, text, model=None):

        ele = self.find_element(loc, model)

        self.logger.info(f'在"{model}"输入"{text}"')
        try:
            ele.send_keys(text)
        except:
            self.logger.exception(f'"{model}"输入失败')
            raise


    def clean_inputText(self, loc, model=None):
        ele = self.find_element(loc, model)

        self.logger.info(f'清除"{model}"')
        try:
            ele.clear()
        except:
            self.logger.exception(f'"{model}"清除失败')
            raise


    def click_element(self, loc, model=None):
        ele = self.find_element(loc, model)
        self.logger.info(f'点击"{model}"  ')
        try:
            ele.click()
        except:
            self.logger.exception(f'"{model}"点击失败')

            raise


    def get_text(self, loc, model=None):
        ele = self.find_element(loc, model)

        try:
            text = ele.text
            self.logger.info(f'获取"{model}"内容"{text}"')
            return text
        except:
            self.logger.exception(f'获取"{model}"内容失败')

            raise


    def get_driver(self):
        return self.driver

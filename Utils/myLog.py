# -*- coding: utf-8 -*-
import logging
import os
import time


class MyLog(object):

    def __init__(self, logger=None):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        log_path = os.path.join(os.path.dirname(cur_path), f'Logs')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        now_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        my_log_path = os.path.join(os.path.dirname(cur_path), f'Logs\\{now_date}')
        if not os.path.exists(my_log_path):
            os.mkdir(my_log_path)
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        now_time = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        log_name = os.path.join(my_log_path, f'{now_time}.log')
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s [line:%(lineno)d]: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getLog(self):
        return self.logger


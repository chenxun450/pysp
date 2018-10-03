# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Browser():

    def __init__(self):
        dcap = DesiredCapabilities.PHANTOMJS
        dcap['browserName'] = 'chrome'
        dcap["platform"] = 'win32'
        dcap["version"] = "win32 chrome 61.0"
        dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        #"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
        # 设置user-agent请求头
        dcap["phantomjs.page.settings.loadImages"] = False  # 禁止加载图片
        self.dr = webdriver.PhantomJS(desired_capabilities=dcap)
        #dr.set_page_load_timeout(15)

    def get_html(self,url):

        self.dr.get(url)
        time.sleep(2)

        html = self.dr.page_source
        return html

    def shotcut(self):
        self.dr.save_screenshot('1.png')
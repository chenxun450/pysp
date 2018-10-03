# -*- coding: utf-8 -*-
import scrapy


class DatiyispiderSpider(scrapy.Spider):
    name = 'datiyispider'
    allowed_domains = ['datiyi.com']
    start_urls = ['http://datiyi.com/']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy


class ExamwspiderSpider(scrapy.Spider):
    name = 'examwspider'
    allowed_domains = ['www.examw.com/zikao/moniti']
    start_urls = ['http://www.examw.com/zikao/moniti/']

    def parse(self, response):
        urlist = response.xpath("//div[position()>7]/div/ul/li/a").extract()
        for ur in urlist:
            url = "http://www.examw.com/" + ur
            yield scrapy.Request(url,callback=self.get_sub)

    def get_sub(self,response):
        ali = response.xpath("//div[@id='List']/li/a[contains(text(),'汇总')]")
        bli = response.xpath( "//div[@id='List']/li/a[contains(text(),'自考各科')]|//div[@id='List']/li/a[contains(text(),'公共课')]")
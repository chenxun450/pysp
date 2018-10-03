# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from bs4 import BeautifulSoup as bs4
import os
import re


class Zikao5Spider(scrapy.Spider):
    name = 'zikao5'
    allowed_domains = ['zikao5.com']
    start_urls = ['http://zikao5.com/forum.php?gid=100']

    cookies = {
        'JaTv_2132_saltkey': 'eZgVIuve',
        'JaTv_2132_lastvisit': '1513233483',
        'JaTv_2132_nofavfid': '1',
        'JaTv_2132_auth': 'd366XV7KWHNMd7TtQfY7VUcgNg%2BRG8vAbWcZ0t2rzfRK2l2Wo%2BN%2BRAPGwdwUCX4Arg3%2FUyxDdPdLuNKdOMUfNtzfaXo',
        'JaTv_2132_lastcheckfeed': '161190%7C1514355742',
        'JaTv_2132_home_diymode': '1',
        'JaTv_2132_ulastactivity': 'c002Hv0KRC2kE8BKUE%2FTELknO6rcfC%2B2qLJJ6IDwE61Wsm1UbZHk',
        'JaTv_2132_st_t': '161190%7C1514425902%7C76ba1e5f25a274d490a11381e30fb220',
        'JaTv_2132_forum_lastvisit': 'D_448_1513827817D_220_1513828597D_75_1513828604D_104_1513828663D_206_1513828846D_952_1513828877D_170_1514357716D_204_1514363898D_212_1514366550D_58_1514425710D_200_1514425717D_101_1514425776D_162_1514425902',
        'JaTv_2132_visitedfid': '162D101D200D58D212D204D170D952D206D104D75D557D448',
        'JaTv_2132_lip': '119.123.12.78%2C1514428375',
        'JaTv_2132_st_p': '161190%7C1514428968%7C78c213a7e0b87770e5617542503db000',
        'JaTv_2132_viewid': 'tid_292842',
        'JaTv_2132_sid': 'tc263p',
        'JaTv_2132_checkpm': '1',
        'JaTv_2132_sendmail': '1',
        'JaTv_2132_lastact': '1514428974%09misc.php%09patch'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url,cookies=self.cookies,callback=self.parse)

    def parse(self, response):

        p = re.compile(r'\d.*?年\d.*?月.*?试题.*?答案.*?')
        soup = bs4(response.text,'lxml')
        ali = soup.find_all("a",text=p)

        for a in ali:
            url0 = "http://zikao5.com/" + a.attrs['href']

            yield scrapy.Request(url0,callback=self.get_subli)

    def get_subli(self, response):

        p = re.compile(r'.*?全国自考试题.*?')
        p1 = re.compile(r'\d.*?年\d.*?月.*?试题.*?')
        soup = bs4(response.text,'lxml')
        soup1 = bs4(response.text,'lxml')

        bli1 = list(set(soup1.find_all('a',text=p1)) - set(soup.find_all('a',text=p)))
        ur = response.xpath('//*[@id="fd_page_bottom"]/div/a[@class="nxt"]/@href').extract()

        for a1 in bli1:
            url1 = "http://zikao5.com/" + a1.attrs['href']
            print(url1)
            yield scrapy.Request(url1,callback=self.get_docurl)

        if len(ur):

            url = "http://zikao5.com/" + ur[0]
            print(url)
            yield scrapy.Request(url,callback=self.get_subli)

    def get_docurl(self,response):
        print("正在获取文件下载链接...")

        soup = bs4(response.text,'lxml')
        p = re.compile(r'\.doc')
        p1 = re.compile(r'\.pdf')
        ali = soup.find_all('a', text=p,)
        bli = list(set(ali))
        cli = list(set(soup.find_all('a',text=p1)))

        if len(ali):
            for a in bli:
                url = "http://zikao5.com/" + a.attrs['href']
                p = re.compile(r"试题")
                filename = p.split(a.string)[0]
                path = './zhenti/doc/' + filename + '.doc'
                if os.path.exists(path):
                    print("该文件已下载～～")
                    continue
                meta = {'name': path}
                yield scrapy.Request(url,callback=self.down_doc,meta=meta)
        elif len(cli):
            for a in cli:
                url = "http://zikao5.com/" + a.attrs['href']
                p = re.compile(r"试题")
                filename = p.split(a.string)[0]
                path = './zhenti/pdf/' + filename + '.pdf'
                if os.path.exists(path):
                    print("该文件已下载～～")
                    continue
                meta = {'name': path}
                yield scrapy.Request(url, callback=self.down_doc, meta=meta)

    def down_doc(self,response):
        print("正在下载文件》》》")
        cont = response.body
        if not os.path.exists('./zhenti/'):
            os.mkdir('./zhenti/')
            os.mkdir('./zhenti/doc/')
            os.mkdir('./zhenti/pdf/')
        filename = response.meta['name']
        with open(filename,'wb') as f:
            f.write(cont)

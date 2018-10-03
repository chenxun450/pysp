# -*- coding:utf-8 -*-

import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}
# patterns_ti = re.compile('')


def get_html(url):

    response = requests.get(url,headers=headers)

    html = response.content
    # status_code = response.status_code

    return html


def main():
    url = 'http://img02.exam8.com/wantiku/zhenti/zikao/2017/0001.html'
    html = get_html(url)
    print(type(html))
    # dom = etree.HTML(html)
    # dom.xpath('')
    # soup = BeautifulSoup(html)
    # soup.find_all()
    with open('html1.html','wb') as f:
        f.write(html)
    f.close()

if __name__ == "__main__":
    main()

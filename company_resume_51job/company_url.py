#!/use/bin/env python
# -*- coding: utf-8 -*-
import requests
import redis
import os
from lxml import html

REDIS_HOST = os.getenv('REDIS_DB_HOST')
REDIS_PORT = int(os.getenv('REDIS_DB_PORT'))


redis_q = redis.StrictRedis(connection_pool=redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0))


header_data = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Host': 'www.51job.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'

               }

url = input('Please enter a company needs to access the URL address: ').strip()

try:
    for i in range(1, 1000):
        request = requests.post(url=url, data={"pageno": i, "hidTotal": '1008'}, headers=header_data).content
        selector = html.fromstring(request)
        url_group = selector.xpath('//p[@class="t1"]/a/@href')
        print("<--------------------------------------------------------------------------------------------------------------*")
        print('The {0} Page, URL is: {1}'.format(i, url_group))
        print("*-------------------------------------------------------------------------------------------------------------->")
        for urls in url_group:
            redis_q.lpush('51job:start_urls', urls)
except:
    pass
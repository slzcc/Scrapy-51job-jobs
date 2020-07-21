#!/use/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
import requests
import urllib.parse
import redis
import os
import threading

REDIS_HOST = os.getenv('REDIS_DB_HOST')
REDIS_PORT = int(os.getenv('REDIS_DB_PORT'))

threads = []

redis_q = redis.StrictRedis(connection_pool=redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0))

class TaskThread(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.Data = data

    def run(self):
        global redis_q
        locks.acquire()
        url = self.Data.xpath('p/span/a/@href')[0]
        redis_q.lpush('51job:start_urls', url)
        locks.release()

def PositionUrl(Html):
    selector = html.fromstring(Html)
    position = selector.xpath('//div[@id="resultList"]/div[@class="el"]')
    for i in position:
        T = TaskThread(i)
        T.start()
        threads.append(T)
    for t in threads:
        t.join()


print("Please according to the prompt to input, must strictly careful operation in order to avoid waste your how many repair operations.")
print("Please enter 'http://www.51job.com/' website for company name to crawl, must be the full name, it doesn't matter too much or you will climb to the company requirements.")
Company_name = urllib.parse.quote(input("Please enter the need to search the company name: "))
Pages = 1

urls = 'http://search.51job.com/list/000000,000000,0000,00,9,99,{0},2,{1}.html'.format(Company_name, Pages)

Request = requests.get(url=urls).content

selector = html.fromstring(Request)

#NumberPages = selector.xpath('//div[@class="dw_table"]/div[@class="dw_tlc"]/div[@class="rt"]/text()')[2].split('/ ')[1]
NumberPages = selector.xpath('//div[@class="dw_table"]/div[@class="dw_tlc"]/div[@class="rt"]/text()')[3].split('\xa0/\xa0')[1]

for i in range(0, int(NumberPages)+1):
    urls = 'http://search.51job.com/list/000000,000000,0000,00,9,99,{0},2,{1}.html'.format(Company_name, i)
    print(urls)
    Request = requests.get(url=urls).content
    locks = threading.Lock()
    PositionUrl(Request)

print("执行完毕请查看 Redis 队列信息.")
# 51job 爬取企业岗位信息

需要准备的服务:
  * Redis
  * Elasticsearch

## 内置参数说明
爬虫已经使用 Docker 封装好，只需要调用所需的环境变量更改服务地址等信息。
Redis 服务地址
```
REDIS_DB_HOST=127.0.0.1
REDIS_DB_PORT=6379
```
Elasticsearch 服务地址以及 index 名称
```
ELASTICSEARCH_DB_SERVER=http://localhost:9200
ELASTICSEARCH_DATA_INDEX=scrapy-51job
ELASTICSEARCH_DATA_TYPE=item
```
## 准备 URL 地址
首先需要搜索公司或者职位名称获取 `URL` 爬虫所需地址，这里只需要执行内部方法即可
```
$ docker run --net host --rm -it -e REDIS_DB_HOST=127.0.0.1 -e ELASTICSEARCH_DB_SERVER=http://localhost:9200 registry.aliyuncs.com/slzcc/scrapy-51job-jobs:elasticsearch company_resume_51job/company_name.py
```
>注意: 这里需要输入的是准确的公司全面，否则会有很多不相干的信息被爬取，如果是职位名称则没任何问题，只要在浏览器当中看到的所有信息都会被爬取下来。

## 运行服务
服务的运行和准备 `URL` 地址并没有直接的关系，如果 Redis 队列中没有 `URL` 地址，则会一直等待。
```
$ docker run --net host -d  -e REDIS_DB_HOST=127.0.0.1 -e ELASTICSEARCH_DB_SERVER=http://localhost:9200 registry.aliyuncs.com/slzcc/scrapy-51job-jobs:elasticsearch
```

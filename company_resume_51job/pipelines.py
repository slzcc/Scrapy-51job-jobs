# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
from scrapy.conf import settings
from datetime import datetime


class CompanyResume51JobPipeline(object):
    def __init__(self):
        self.server = settings['ELASTICSEARCH_DB_SERVER']
        self.index_name = settings['ELASTICSEARCH_DATA_INDEX']
        self.type_name = settings['ELASTICSEARCH_DATA_TYPE']
        self.es = Elasticsearch([self.server])

    def process_item(self, item, spider):
        data = dict(item)
        data['@timestamp'] = datetime.now()
        self.es.index(index=self.index_name, doc_type=self.type_name, body=data)
        self.es.indices.refresh(index=self.index_name)
        return item
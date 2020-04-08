# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import json


class QiushibaikePipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient('localhost', 27017)
        self.db = self.connection.scrapy
        self.collection = self.db.qiushibaike

    def process_item(self, item, spider):
        if not self.connection or not item:
            return None
        self.collection.save(item)
        # data = json.dumps(list(item.items()), ensure_ascii=False, indent=4)
        # print(data)
        print(item.items())
        return item

    def __del__(self):
        if self.connection:
            self.connection.close()


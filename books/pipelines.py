# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class BooksPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        my_setting = settings.get("MY_SETTING")
        return cls(my_setting)

    def __init__(self, my_setting):
        client = MongoClient(my_setting['MONGODB_SERVER'], my_setting['MONGODB_PORT'])
        db = client[my_setting['MONGODB_DB']]
        self.collection = db.collection_names(my_setting['MONGODB_COLLECTION'])

    def process_item(self, item, spider):

        spec = {"subject_id": item["subject_id"]}
        self.collection.update(spec, {'$set': dict(item)}, True)
        return item

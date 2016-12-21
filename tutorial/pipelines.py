# -*- coding: utf-8 -*-

#管道存储数据
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import datetime
from pymongo import MongoClient
from scrapy import log

from tutorial.settings import MONGO_URI, PROJECT_DIR


class TutorialPipeline(object):
    def __init__(self, mongo_uri, mongo_db, image_dir):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.image_dir = image_dir
        self.client = None
        self.db= None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=MONGO_URI,
            mongo_db='longshihan',
            image_dir=os.path.join(PROJECT_DIR, 'images')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if not os.path.exists(self.image_dir):
            os.mkdir(self.image_dir)

    def close_spider(self, spider):

        self.client.close()



    def process_item(self, item, spider):
        book_detail = {
            'book_name': item.get('book_name'),
            'alias_name': item.get('alias_name', []),
            'author': item.get('author', []),
            'book_description': item.get('book_description', ''),
            'book_covor_image_path': item.get('book_covor_image_path', ''),
            'book_covor_image_url': item.get('book_covor_image_url', ''),
            'book_download': item.get('book_download', []),
            'book_file_url': item.get('book_file_url', ''),
            'book_file': item.get('book_file', ''),
            'original_url': item.get('original_url', ''),
            'update_time': datetime.datetime.utcnow(),
        }
        result = self.db['book_detail'].insert(book_detail)
        item["mongodb_id"] = str(result)
        log.msg("Item %s wrote to MongoDB database %s/book_detail" %
                (result, self.MONGODB_DB),
                level=log.DEBUG, spider=spider)
        return item

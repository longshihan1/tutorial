#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class WoaiduCrawlerItem(scrapy.Item):
    mongodb_id = Field()
    book_name = Field()
    alias_name = Field()
    author = Field()
    book_description = Field()
    book_covor_image_path = Field()
    book_covor_image_url = Field()
    book_download = Field()
    book_file_url = Field()
    book_file = Field()  # only use for save tho single mongodb
    book_file_id = Field()  # only use for save to shard mongodb
    original_url = Field()

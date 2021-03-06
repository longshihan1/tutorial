# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request
from scrapy.selector import HtmlXPathSelector

from tutorial.items import WoaiduCrawlerItem
from tutorial.utils.select_result import list_first_item, clean_url, strip_null, deduplication


class DmozSpider(scrapy.Spider):
    name = "woaidu"
    start_urls = (
        'http://www.woaidu.org/sitemap_1.html',
    )

    def parse(self, response):
        response_selector = HtmlXPathSelector(response)
        next_link = list_first_item(response_selector.select(u'//div[@class="k2"]/div/a[text()="下一页"]/@href').extract())
        if next_link:
            next_link = 'http://www.woaidu.org'+next_link
            yield Request(url=next_link, callback=self.parse)

        for detail_link in response_selector.select(u'//div[contains(@class,"sousuolist")]/a/@href').extract():
            if detail_link:
                detail_link ='http://www.woaidu.org'+detail_link
                yield Request(url=detail_link, callback=self.parse_detail)

    def parse_detail(self, response):
        woaidu_item = WoaiduCrawlerItem()

        response_selector = HtmlXPathSelector(response)
        woaidu_item['book_name'] = list_first_item(
            response_selector.select('//div[@class="zizida"][1]/text()').extract())
        woaidu_item['author'] = [
            list_first_item(response_selector.select('//div[@class="xiaoxiao"][1]/text()').extract())[5:].strip(), ]
        woaidu_item['book_description'] = list_first_item(
            response_selector.select('//div[@class="lili"][1]/text()').extract()).strip()
        woaidu_item['book_covor_image_url'] = list_first_item(
            response_selector.select('//div[@class="hong"][1]/img/@src').extract())

        download = []
        for i in response_selector.select('//div[contains(@class,"xiazai_xiao")]')[1:]:
            download_item = {}
            download_item['url'] = \
                strip_null( \
                    deduplication( \
                        [ \
                            list_first_item(i.select('./div')[0].select('./a/@href').extract()), \
                            list_first_item(i.select('./div')[1].select('./a/@href').extract()) \
                            ] \
                        ) \
                    )

            download_item['progress'] = list_first_item(i.select('./div')[2].select('./text()').extract())
            download_item['update_time'] = list_first_item(i.select('./div')[3].select('./text()').extract())
            download_item['source_site'] = \
                [ \
                    list_first_item(i.select('./div')[4].select('./a/text()').extract()), \
                    list_first_item(i.select('./div')[4].select('./a/@href').extract()) \
                    ] \

            download.append(download_item)

        woaidu_item['book_download'] = download
        woaidu_item['original_url'] = response.url

        yield woaidu_item
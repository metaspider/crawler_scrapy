# -*- coding: utf-8 -*-
import scrapy


class BtSpider(scrapy.Spider):
    name = 'bt'
    allowed_domains = ['tieba.com']
    start_urls = ['http://tieba.com/']

    def parse(self, response):
        pass

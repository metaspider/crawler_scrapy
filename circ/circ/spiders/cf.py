# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class CfSpider(CrawlSpider):
    name = 'cf'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://bxjg.circ.gov.cn/web/site0/tab5240/module14430/page1.htm']

    # 定义提取url地址规则
    rules = (
        # Rule: 是个类
        # LinkExtractor: 链接提取器，提取 url 地址
        # callback: 提取出来的url地址的 response 会交给 callback
        # follow: 当前url地址的响应是否重新经过 Rules 来提取 url 地址
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item', follow=False),  # 提取这一页详情的地址
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+.htm'), follow=True),  # 提取下一页地址
    )

    # parse函数有特殊功能，不能定义
    def parse_item(self, response):
        item = {}
        # item['title'] = response.xpath('//table/tbody/tr/td/span/a/text()').extract()
        item['title'] = re.findall(r'<!--TitleStart-->(.*?)<!--TitleEnd-->',response.body.decode(), re.S)[0]
        # item['data'] = response.xpath('//table/tbody/tr/td[last]/text()').extract()
        item['data'] = re.findall(r'\d{2,}-\d{2,}-\d{2,}', response.text, re.S)
        print(item)


# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy

class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['list.suning.com']
    start_urls = ['http://list.suning.com']

    def parse(self, response):
        div_list = response.xpath('//div[@id="502282"]/div')
        for div in  div_list:
            item = {}
            item['cate'] = div.xpath('./div[1]/a/text()').extract_first()
            # 小组分组
            a_list = div.xpath('./div[2]/a')
            for a in a_list:
                item['s_cate'] = a.xpath('./text()').extract_first()
                item['s_href'] = 'http:' + a.xpath('./@href').extract_first()
                if item['s_href'] is not None:
                    item['s_url'] = item['s_href']
                    yield scrapy.Request(
                        url=item['s_url'],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        item = response.meta["item"]
        # 图书列表页分组
        li_list = response.xpath('//*[@id="product-list"]/ul/li')
        for li in li_list:
            item['book_name'] = li.xpath('.//div[@class="title-selling-point"]/a/text()').extract_first()
            item['book_image'] = 'http:' + li.xpath('.//div[@class="img-block"]/a/img/@src').extract_first()
            item['book_auth'] = li.xpath('.//div[@class="img-block"]/a/@title').extract_first()
            item['book_url'] = 'http:' + li.xpath('.//div[@class="img-block"]/a/@href').extract_first()
            print(item)
            with open('./suning.txt', 'a', encoding='utf-8') as f:
                f.write(str(item))
                f.write('\n')



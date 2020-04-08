# -*- coding: utf-8 -*-
import scrapy
from qiushibaike.items import QiushibaikeItem


class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    def parse(self, response):
        print('\nstart  {} ......\n'.format(response.url))
        content_left_div = response.xpath('//*[@id="content-left"]')
        content_list_div = content_left_div.xpath('./div')

        for content_div in content_list_div:
            try:
                item = QiushibaikeItem()
                try:
                    item['author'] = content_div.xpath('./div/a[2]/h2/text()').get().strip()
                except:
                    item['author'] = content_div.xpath('./div/span[2]/h2/text()').get().strip()
                # item['content'] = "".join(content_div.xpath('./a/div[@class="content"]/span/text()').getall()).strip().replace('\n', '')
                item['content'] = "".join(content_div.xpath('./a[contains(@href, "article")]/div[@class="content"]/span/text()').getall()).strip().replace('\n', '')
                item['_id'] = content_div.attrib['id']
                yield item
            except Exception as e:
                print(response.url)
                print("item error", e.args)

        next_page = response.xpath('//*[@id="content-left"]/ul/li[last()]/a/@href').get()

        if next_page:
            next_page = 'https://www.qiushibaike.com' + next_page
            yield scrapy.Request(url=next_page, callback=self.parse)


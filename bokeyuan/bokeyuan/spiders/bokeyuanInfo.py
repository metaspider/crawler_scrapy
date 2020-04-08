# -*- coding: utf-8 -*-
import scrapy
from bokeyuan.settings import PAGE_NUM
import re
from datetime import datetime


class BokeyuaninfoSpider(scrapy.Spider):
    name = 'bokeyuanInfo'
    allowed_domains = ['www.cnblogs.com']
    start_url = 'https://www.cnblogs.com/sitehome/p/{page}'.format(page=PAGE_NUM)
    start_urls = [start_url, ]

    def parse(self, response):
        # 输出对应页码的内容
        # soup = BeautifulSoup(response.text, 'lxml')
        # html = soup.prettify()
        # # print(html)
        # print(response.text)

        post_items = response.xpath('//div[@id="post_list"]/div[@class="post_item"]')  # 遍历每个博客的信息
        for post_item in post_items:
            articleInfo = dict()

            # 这些信息要输出到指定地址的mysql数据库中
            # 作者
            articleInfo['author'] = post_item.xpath('.//a[@class="lightblue"]/text()').get().strip()
            # 发布时间
            issue_time = post_item.xpath('.//div[@class="post_item_foot"]/text()').getall()
            issue_time = ' '.join(''.join(issue_time).strip().split()[-2:])
            articleInfo['issue_time'] = datetime.strptime(issue_time, '%Y-%m-%d %H:%M')  # 将发布时间转化为datetime格式
            # print(str(articleInfo['issue_time']))
            # 评论数
            num_comment = post_item.xpath('.//span[@class="article_comment"]/a[@class="gray"]/text()').get().strip()
            articleInfo['num_comment'] = int(re.findall('(\d+)', num_comment)[0])
            # 阅读数
            num_read = post_item.xpath('.//span[@class="article_view"]/a[@class="gray"]/text()').get().strip()
            articleInfo['num_read'] = int(re.findall('(\d+)', num_read)[0])
            # 标题
            articleInfo['title'] = post_item.xpath('.//a[@class="titlelnk"]/text()').get().strip()
            # 推荐数
            articleInfo['num_recommend'] = int(post_item.xpath('.//span[@class="diggnum"]/text()').get().strip())

            yield articleInfo

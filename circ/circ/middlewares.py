# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from circ import settings
import random

class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        # print(spider.settings)
        user_agent = random.choice(spider.settings.get('USER_AGENT_LIST'))
        # ua = random.choice(settings.USER_AGENT_LIST)
        request.headers["User-Agent"] = user_agent

class CheckUserAgent:
    def process_response(self, request, response, spider):
        # print(dir(response.request))
        print(request.headers['User-Agent'])
        return response

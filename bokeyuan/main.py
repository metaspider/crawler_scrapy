"""
Function : 爬取博客园任意一页的博客信息，页数由 settings 文件任意指定
"""

from scrapy.cmdline import execute

execute('scrapy crawl bokeyuanInfo'.split())

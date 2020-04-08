# -*- coding: utf-8 -*-

BOT_NAME = 'fengye'  # 项目名称

SPIDER_MODULES = ['fengye.spiders']
NEWSPIDER_MODULE = 'fengye.spiders'

START_URL_FILES = "./fyeds_url.txt"    # url 文件路径

LOG_LEVEL = "WARNING"

IP_PROXY_ENABLE = False
IP_PROXY = "111.231.73.229:7000"

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'

ROBOTSTXT_OBEY = False  # 关闭robots协议

CONCURRENT_REQUESTS = 5   # 最带连接数

FILE_SINGLE_PAGE = "./file_single_page"
FILE_LIST_PAGE = "./file_list_page"
FILE_LOWER_SHELF = "./file_lower_shelf"
FILE_ADD_WEIXIN = "./file_add_weixin"
FILE_XIAO_SHUO = "./file_xiao_shuo"


# DOWNLOAD_DELAY = 3  # 延迟

COOKIES_ENABLED = False  # cookie状态

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

SPIDER_MIDDLEWARES = {
   'fengye.middlewares.FengyeSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
   'fengye.middlewares.FengyeDownloaderMiddleware': 543,
}
if IP_PROXY_ENABLE:
    DOWNLOADER_MIDDLEWARES['fengye.middlewares.IP_ProxyMiddleware'] = 300

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

ITEM_PIPELINES = {
   'fengye.pipelines.FengyePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

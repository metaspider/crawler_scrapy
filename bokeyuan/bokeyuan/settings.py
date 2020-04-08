# -*- coding: utf-8 -*-

"""
这里为 bokeyuan 爬虫的 配置文件
"""

# 爬虫可调参数配置
PAGE_NUM = 5  # 要爬取博客园的哪一页

# mysql数据库参数配置信息
host = 'localhost'  # 设置远程数据库地址
user = 'root'
password = '123456'

# mysql数据库数据库名称信息
db_name = 'bokeyuan'  # 数据库名称
table_name = 'ArticleInfo'  # 数据表名称

# IP代理 , 此处代理为对目标网站重定向检测后的可用IP代理，但可用性时间仍然很快过时
IP_ENABLE = False  # 默认不使用IP代理
IP_POOL = [
    "116.196.90.181:3128",
    "212.188.66.218:8080",
    "194.1.193.226:35646",
]

LOG_LEVEL = "WARNING"  # 禁止日志内容输出警告信息

BOT_NAME = 'bokeyuan'  # 机器人名称

SPIDER_MODULES = ['bokeyuan.spiders']
NEWSPIDER_MODULE = 'bokeyuan.spiders'

# 用户代理设置
USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'

# 遵从爬虫协议
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'bokeyuan.middlewares.BokeyuanSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'bokeyuan.middlewares.BokeyuanDownloaderMiddleware': 543,
}
if IP_ENABLE:  # 如果开启IP代理，就调用爬虫IP代理中间件
    DOWNLOADER_MIDDLEWARES['bokeyuan.middlewares.MyproxiesSpiderMiddleware'] = 100

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'bokeyuan.pipelines.BokeyuanPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

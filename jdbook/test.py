# !/usr/bin/env python3  # linux下生效
# -*- ecoding: utf-8 -*-
# @TestEnv: python 3.6.0
# @ModuleName: test
# @Function: 
# @Author: 漫天丶飞雪
# @Date: 2019/7/14 17:07

from scrapy.cmdline import execute

execute("scrapy crawl jd -o ../saveInfo.jl".split())


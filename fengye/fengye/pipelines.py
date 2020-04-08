# -*- coding: utf-8 -*-

import os
import re
import json
from logging import getLogger

from fengye.spiders.fengye_web import PageType
from fengye.settings import FILE_SINGLE_PAGE
from fengye.settings import FILE_LIST_PAGE
from fengye.settings import FILE_LOWER_SHELF
from fengye.settings import FILE_ADD_WEIXIN
from fengye.settings import FILE_XIAO_SHUO


class FengyePipeline(object):

    def __init__(self):
        """ 创建单页面文件 """
        self.i = 0
        if not os.path.exists(FILE_SINGLE_PAGE):
            os.mkdir(FILE_SINGLE_PAGE)
        """ 创建多页面文件 """
        if not os.path.exists(FILE_LIST_PAGE):
            os.mkdir(FILE_LIST_PAGE)
        """ 创建商品下架页面 """
        if not os.path.exists(FILE_LOWER_SHELF):
            os.mkdir(FILE_LOWER_SHELF)
        """ 创建商品添加微信页面 """
        if not os.path.exists(FILE_ADD_WEIXIN):
            os.mkdir(FILE_ADD_WEIXIN)
        """ 创建商品小说页面 """
        if not os.path.exists(FILE_XIAO_SHUO):
            os.mkdir(FILE_XIAO_SHUO)

    def process_item(self, item, spider):
        """ 项目结果处理 """
        # 商品下架
        if item.get("page_type") == PageType.LOWER_SHELF:
            self.process_lower_shelf(item=item)
        # 单页面商品
        if item.get("page_type") == PageType.SINGLE_PAGE:
            self.process_single_page(item=item)
        # 多页面商品
        if item.get("page_type") == PageType.LIST_PAGE:
            self.process_list_page(item=item)
        # 添加上加微信看结果
        if item.get("page_type") == PageType.WEIXIN:
            self.process_add_weixin(item=item)
        # 页面时小说
        if item.get("page_type") == PageType.XIAO_SHUO:
            self.process_xiao_shuo(item=item)

        return item

    def process_single_page(self, item):
        """ 处理单页面 """
        file_path = FILE_SINGLE_PAGE+"/"+self.process_filename(title=item.get("url"))+".txt"
        # item["page_type"] = item.get("page_type").value
        item.pop("page_type")  # 删除判断单多页的枚举类型方法
        item_content = json.dumps(item, indent=4, ensure_ascii=False)
        # print(item)
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(item_content)
        print("URL: %s is single page, html page is saving over ." % item.get("url"))

    def process_list_page(self, item):
        """ 处理多页面 """
        # item.pop("page_type")  # 删除判断单多页的枚举类型方法
        # item = json.dumps(item, indent=4, ensure_ascii=False)
        # print(item)
        # item = item.get("URL_LEN")
        # print(self.i, type(item.get("LIST_PAGE_CONTENT")), len(item.get("LIST_PAGE_CONTENT")))
        # print(item)
        for num, li in enumerate(item.get("LIST_PAGE_CONTENT")):
            try:
                # item["LIST_PAGE_CONTENT"][num] = PageType.LIST_PAGE.value
                item["LIST_PAGE_CONTENT"][num].pop("page_type")
                # print(li)
            except Exception as e:
                """ 报错说明遍历到了非字典的部分 """
                print("ERROR:", e.args)
        item_content = json.dumps(item.get("LIST_PAGE_CONTENT"), indent=4, ensure_ascii=False)
        file_path = FILE_LIST_PAGE + "/" + self.process_filename(title=item.get("url")) + ".txt"
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(item_content)
        print("URL: %s is list page, html page is saving over ." % item.get("url"))

    def process_lower_shelf(self, item):
        """ 处理商品下架 """
        file_path = FILE_LOWER_SHELF+"/"+self.process_filename(title=item.get("url"))+".html"
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(item.get("html"))
        print("URL: %s is lower shelf, html page is saving over ." % item.get("url"))

    def process_add_weixin(self, item):
        """ 处理商品下架 """
        file_path = FILE_ADD_WEIXIN+"/"+self.process_filename(title=item.get("url"))+".txt"
        item_content = {
            "url": item.get("url"),
            "page_type": item.get("page_type").value,
            "html": item.get("html"),
        }
        item_content = json.dumps(item_content, indent=4, ensure_ascii=False)
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(item_content)
        print("URL: %s is add weixin, html page is saving over ." % item.get("url"))

    def process_xiao_shuo(self, item):
        """ 处理商品下架 """
        file_path = FILE_XIAO_SHUO+"/"+self.process_filename(title=item.get("url"))+".txt"
        item_content = {
            "url": item.get("url"),
            "page_type": item.get("page_type").value,
            "html": item.get("html"),
        }
        item_content = json.dumps(item_content, indent=4, ensure_ascii=False)
        with open(file=file_path, mode="w", encoding="utf-8") as f:
            f.write(item_content)
        print("URL: %s is xiao shuo, html page is saving over ." % item.get("url"))

    def process_filename(self, title, handle_underline=True):
        """ 替换掉不能作为文件名的字符 """
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        title = re.sub(rstr, "_", title)  # 替换为下划线
        if handle_underline:
            title = re.sub("(_+)", "_", title)
        return title



# -*- coding: utf-8 -*-

from enum import Enum, unique  # 枚举
from urllib import parse
import os
import re
import json
import time

from bs4 import BeautifulSoup
import scrapy

from fengye.settings import START_URL_FILES
from fengye.settings import FILE_SINGLE_PAGE

@unique
class PageType(Enum):
    SINGLE_PAGE = "单页面"
    LIST_PAGE = "多页面"
    LOWER_SHELF = "商品下架"
    WEIXIN = "添加微信的广告"
    XIAO_SHUO = "页面内容是小说"

class FengyeWebSpider(scrapy.Spider):
    name = 'fengye_web'
    allowed_domains = ['fyeds1.com']

    def start_requests(self):
        """ 重写 start_requests """
        with open(START_URL_FILES, "r", encoding="utf-8") as f:
            URLS_LINES = f.readlines()
        URLS = [url.strip() for url in URLS_LINES if url.strip()]
        try:
            local_keywords_sort = self.get_file_list(FILE_SINGLE_PAGE)
            start_keyword_name = local_keywords_sort[-1].split('.txt')[0]
            start_keyword_num = URLS.index(start_keyword_name) + 1
        except:
            start_keyword_num = 0
        # """
        # 0. https://36f2ebea.fyeds1.com/?ecfrom=together&together_id=199193720&r_id=199193559_d871033d2&qz_gdt=&gdt_vid=
        # https://36f2ebea.fyeds1.com/?r_id=199193720_fce09b530&pagetype=TOGETHER&_bid=2759
        # """
        # URLS = ["https://36f2ebea.fyeds1.com/?r_id=199193720_fce09b530&pagetype=TOGETHER&_bid=2759"]
        URLS = ['https://beta.712c4eb0.fyeds9.com/?r_id=11095789_4413051b6&pagetype=TOGETHER&_bid=2759']
        start_keyword_num = 0
        print("start number %s." % start_keyword_num)
        for URL in URLS[start_keyword_num::]:
            yield scrapy.Request(url=URL, meta={"URL": URL}, dont_filter=True)

    def get_file_list(self, file_path):
        dir_list = os.listdir(file_path)
        if not dir_list:
            return
        else:
            # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
            # os.path.getmtime() 函数是获取文件最后修改时间
            # os.path.getctime() 函数是获取文件最后创建时间
            dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
            # print(dir_list)
            return dir_list

    def soup_Beautiful(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        html_studio = soup.prettify()
        print(html_studio)


    def parse(self, response):
        self.soup_Beautiful(response=response)  # 标准化输出
        print(response)
        # try:
        """ 判断页面类型是属于 1.单页面  2.多页面  3.商品下架 """
        single_or_list = self.get_good_info_type(response=response)
        print("SINGLE OR LIST :  %s" % single_or_list, flush=True)

        # 处理单页面商品
        if single_or_list == PageType.SINGLE_PAGE:
            result = self.handle_single_page(response=response, single_or_list=single_or_list)
            # result = json.dumps(result, indent=4, ensure_ascii=False)
            return result

        # 处理多页面商品
        elif single_or_list == PageType.LIST_PAGE:
            result = self.handle_list_page(response=response, single_or_list=single_or_list)
            # result = json.dumps(result, indent=4, ensure_ascii=False)
            return result

        # 处理下架商品
        elif single_or_list == PageType.LOWER_SHELF:
            return {
                "page_type": single_or_list,
                "url": response.meta.get("URL"),
                "html": self.get_org_data(response=response)
            }

        elif single_or_list in [PageType.WEIXIN, PageType.XIAO_SHUO]:
            return {
                "page_type": single_or_list,
                "url": response.meta.get("URL"),
                "html": self.get_org_data(response=response)
            }

        # except Exception as e:
        #     print("Parse Error:", e.args, response)

    def handle_list_page(self, response, single_or_list):
        """ 多商品页面处理 """
        list_page_html = list(self.get_list_page_all_urls(response=response))
        URL_LEN = len(list_page_html)
        PAGE_CONTENT = {
            "page_type": PageType.LIST_PAGE,
            "url": self.get_page_url(response=response),
            "html": self.get_org_data(response=response),
            "LIST_PAGE_CONTENT": [
                {
                    "URL": self.get_page_url(response=response),
                    "PAGE_TYPE": single_or_list.value,
                    "URLS": list_page_html,
                    "HTML": self.get_org_data(response=response)
                }
            ]
        }
        for URL in list_page_html:
            # print(URL)
            yield scrapy.Request(url=URL, meta={"URL": URL, "URL_LEN": URL_LEN, "PAGE_CONTENT": PAGE_CONTENT}, callback=self.handle_sub_page_of_list_page, dont_filter=True)

    def handle_sub_page_of_list_page(self, response):
        """ 处理多页面中的分页面 """
        print(response)
        """ 判断多页面各个页面是不是属于商品下架 """
        if  self.get_good_info_type(response=response) == PageType.LOWER_SHELF:
            result = {
                "url": self.get_page_url(response=response),
                "status": PageType.LOWER_SHELF.value,
            }
        else:
            result = self.handle_single_page(response=response, single_or_list=PageType.SINGLE_PAGE)
        # result.pop("page_type")
        # result["page_type"] = PageType.LIST_PAGE.value
        # print(result["page_type"], type(result["page_type"]))
        response.meta["PAGE_CONTENT"]["LIST_PAGE_CONTENT"].append(result)
        if len(response.meta["PAGE_CONTENT"]["LIST_PAGE_CONTENT"]) == response.meta.get("URL_LEN"):
            return response.meta["PAGE_CONTENT"]
        else:
            return None

    def handle_single_page(self, response, single_or_list):
        """ 单商品页面处理 """
        source_name = self.get_source_name(response=response)
        goods_info_type = single_or_list.value
        org_data = self.get_org_data(response=response)
        goods_url = self.get_page_url(response=response)
        goods_price = self.get_goods_price(response=response)
        goods_tag = self.get_gooods_tag(response=response)
        goods_description_info = self.get_goods_description_text_info(response=response)
        page_title = self.get_page_title(response=response)
        goods_first_image_url = self.get_goods_first_image_url(response=response)
        structure_data = {
            "PAGE_TITLE": page_title,
            "GOODS_FIRST_IMAGE_URL": goods_first_image_url,
            "GOODS_TAG_CONTENT": goods_tag,
            "GOODS_PRICE": goods_price,
            "GOODS_DESCRIPTION_INFO": goods_description_info,
        }
        return {
            "page_type": single_or_list,
            "source": source_name,
            "url": goods_url,
            "info_type": goods_info_type,
            # "structure_data": str(json.dumps(structure_data, indent=None, ensure_ascii=False)),
            "structure_data": structure_data,
            "org_data": org_data
        }

    def get_source_name(self, response):   # 1.
        """ source    站点名称(fyeds) """
        URL = response.meta.get("URL")
        URL = str(URL)
        if not URL.startswith("http://") and not URL.startswith("https://"):
            URL = "http://" + URL
        NETLOC = parse.urlsplit(URL).netloc
        return NETLOC

    def get_good_info_type(self, response):   # 2.
        """ info_type    获取商品信息类型 ( list / single ; 单商品页面 / 多商品页面 ) """
        """ 判断是否是要添加微信 """

        """ 判断是不是小说 """
        if "继续阅读" in response.text:
            return PageType.XIAO_SHUO

        if "关注商家，请添加商家微信" in response.text:
            return PageType.WEIXIN

        preview_phone = response.xpath('//div[@class="preview-phone"]')
        # goods_not_exists = response.xpath('//body/div/img/@alt').extract_first()
        goods_not_exists = response.xpath('/html/head/title/text()').extract_first()
        """ 判断是否商品下架 """
        if str(goods_not_exists).strip() in ["商品下架啦", "预览失效"] and not preview_phone:
            return PageType.LOWER_SHELF

        """ 判断是的单页面还是多页面 """
        clear_together_module = preview_phone.xpath('./div[@class="clear together-module"]')
        if clear_together_module and preview_phone:   # 多页面
            return PageType.LIST_PAGE
        elif not clear_together_module and preview_phone:   # 单页面
            return PageType.SINGLE_PAGE

    def get_org_data(self, response):   # 4.
        """ 网页的原始HTML信息（org_data） """
        return response.text

    def get_page_url(self, response):  # 5.
        """ 获取商品页面对应的URL """
        return response.meta.get("URL")

    def get_goods_status(self, response):
        """ 获取商品标签，判断是否是下架商品 """
        goods_title = response.xpath('//div[@class="preview-phone"]//p[@style]/text()').extract_first()
        return goods_title

    def get_gooods_tag(self, response):
        """ 获取商品标签 """
        goods_tag = response.xpath('//div[@id="marketingModules"]/p/text()').extract_first()
        return goods_tag

    def get_goods_description_text_info(self, response):
        """ 商品描述文本信息 """
        goods_description_info = response.xpath('//div[@class="preview-phone"]//div/div[@class]/div[@class]/p')
        # re.findall()
        goods_description_info_list = list()
        for p in goods_description_info:
            info = p.xpath('./strong[@style]/text()').extract()
            strong = "".join([item.strip() for item in info])
            goods_description_info_list.append(strong)
        # goods_description_info = [item.strip() for item in goods_description_info if item.strip()]
        goods_description_info_list = [item.strip() for item in goods_description_info_list if item.strip()]
        # return goods_description_info
        return goods_description_info_list

    def get_goods_price(self, response):
        """ 商品首图url,价格 """
        price = response.xpath('//div[@id="marketingModules"]/div[@class="good-price"]/text()').extract()
        price_unit = response.xpath('//div[@id="marketingModules"]/div[@class="good-price"]/span[@style]/text()').extract_first()
        price = [item.strip() for item in price if item.strip()]
        if len(price) > 0:
            if price_unit:
                return price_unit + price[0]
            else:
                return price

        price = response.xpath('//div[@class="ec-form-fields"]/div/ul[@class]/li[@class]/@data-price').extract_first()
        if price:
            goods_proce_unit = "￥"
            if goods_proce_unit not in price:
                return goods_proce_unit + str(price)
        else:
            return "￥0"

    def get_page_title(self, response):
        """ 获取页面TITLE """
        title = response.xpath('/html/head/title/text()').extract_first()
        return title

    def get_goods_first_image_url(self, response):
        """ 获取商品首图URL """
        """ /html/body/div[1]/div[1]/div/img/@src """
        image_url = response.xpath('//body/div[@class="preview-phone"]/div/div/img/@src').extract_first()
        image_url = str(image_url)
        if image_url and image_url.startswith("//"):
            image_url = "https:"+image_url

        return image_url

    def get_list_page_all_urls(self, response):
        """ 获取多页面的所有url列表 """
        LIST_PAGE_URLS = response.xpath('.//div[@class="preview-phone"]/div[@class="clear together-module"]/a[@class="together-link"]/@href').extract()
        # LIST_PAGE_URLS = [for url in LIST_PAGE_URLS ]
        # print(LIST_PAGE_URLS)
        request_page_url = response.meta.get("URL")
        for URL in LIST_PAGE_URLS:
            NEW_URL = parse.urljoin(request_page_url, URL)
            # print(NEW_URL)
            yield NEW_URL
        else:
            return []


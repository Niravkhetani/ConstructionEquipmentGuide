import scrapy
# from fake_headers import Headers
from tutorial.items import Construction
import logging
from scrapinghub import ScrapinghubClient
import requests,json,re
from scrapy.http import HtmlResponse

from scrapy.selector import Selector


class ConstructionList(scrapy.Spider):
    name = "CGList"
    start_urls = ["https://www.constructionequipmentguide.com/"]
    global item
    item = Construction()


    def parse(self, response):
        cat_content = ["Aerial Lifts", "Air Compressors", "Asphalt/Concrete/Paving", "Attachments",
                       "Backhoe Loaders", "Compact Track Loaders", "Compaction Equipment",
                       "Crawlers Dozers", "Crawlers Loaders", "Drills", "Excavators",
                       "Forklifts", "Ligth Towers", "Material Handlers",
                       "Miscellaneous Equipment,Motor Graders", "Off- Highway trucks",
                       "On - Road Trucks", "Pipe Layers", "Power System Generation",
                       "Pumps,Scrapers", "Skid Sxteer Loaders", "Snow Equipment",
                       "Straw Blowers/ Hydroseeders", "Sweepers", "Telehandlers",
                       "Trenching/boring/Cable Pows", "Utility Vehicles", "Welders", "Wheel Dozers",
                       "Wheel Loaders"]
        target = response.xpath("//div/ul/li/a/text()").getall()
        next_cat = []
        nexts = []
        next1 = None
        next2 = None
        for i in cat_content:
            if i in target:
                next_cat.append(response.xpath("//div/ul/li/a[contains(text(),'%s')]/@href" % (str(i))).get())
                nexts.append(response.xpath("//div/ul/li/a[contains(text(),'%s')]/text()" % (str(i))).get())
        for i, j in zip(nexts, next_cat):
            if i == 'Attachments' or i == 'Compaction Equipment' or i == 'Power System Generation':
                next1 = response.urljoin(j)
                yield scrapy.Request(next1, self.used_attachment_item,meta={'category':i})
            else:
                next1 = response.urljoin(j)
                yield scrapy.Request(next1, self.parse_item_list,meta={'category':i})

    def used_attachment_item(self, response):
        used_attachment = response.xpath(
            "//div/ul/li[@class='category']/a/@href").getall()
        for i in used_attachment:
            cat_temp = response.meta.get("category")
            j = response.xpath("div/ul/li[@class='category']/a/text()").get()
            used_attachment_path    = "https://www.constructionequipmentguide.com"+ i
            yield scrapy.Request(used_attachment_path, self.parse_item_list,meta={'category':cat_temp,'category2':j})

    def parse_item_list(self, response):
        collection_items = response.xpath("//div[@class='result machine-listing trackImpression']")
        for construct in collection_items:
            default = ""
            item['item_title'] = construct.xpath("div[@class='machine-details']/div/a/text()").get().strip()
            item['item_url']   = "https://www.constructionequipmentguide.com"+construct.xpath("div[@class='machine-photo']/a/@href").get()
            category1          = response.meta['category'] or default
            category2          = response.meta.get('category2') or default
            item['category'] = {'cat1_name': category1,
                                'cat2_name': category2,
                                'cat1_id': '',
                                'cat2_id': ''
                                }
            item['requrl'] = response.url
            yield item
        next_page = response.xpath('//*[contains(text(),"Next Page")]/@href').get('')
        if next_page:
            next1 = response.urljoin(next_page)
            yield scrapy.Request(next1,self.parse_item_list,meta={'category':category1,'category2':category2})


import scrapy
# from fake_headers import Headers
from tutorial.items import Construction
import logging
from scrapinghub import ScrapinghubClient
import requests,json,re
from scrapy.http import HtmlResponse




class ConstructionList(scrapy.Spider):
    name = "CGList"
    url = "https://www.constructionequipmentguide.com/"
    custom_settings = {"FEEDS": {"results.csv": {"format": "csv"}}}
    global item
    item = Construction()



    def start_requests(self):
        yield scrapy.Request(self.url, self.parse_list_category)

    def parse_list_category(self, response):
        cat_content = ["Aerial Lifts", "Air Compressors", "Asphalt/Concrete/Paving", "Attachments",
                       "Backhoe Loaders", "Compact Track Loaders", "Compaction Equipment",
                       "Crawlers Dozers", "Crawlers Loaders", "Drills", "Excavators",
                       "Forklifts", "Ligth Towers", "Material Handlers",
                       "Miscellaneous Equipment,Motor Graders", "Off- Highway trucks",
                       "On - Road Trucks", "Pipe Layers", "Power System Generation",
                       "Pumps,Scrapers", "Skid Steer Loaders", "Snow Equipment",
                       "Straw Blowers/ Hydroseeders", "Sweepers", "Telehandlers",
                       "Trenching/boring/Cable Pows", "Utility Vehicles", "Welders", "Wheel Dozers",
                       "Wheel Loaders"]
        category = response.xpath("//div/ul/li/a/@href").get()
        target = response.xpath("//div/ul/li/a/text()").getall()
        next_cat = []
        nexts = []
        next1 = None
        for i in cat_content:
            if i in target:
                next_cat.append(response.xpath("//div/ul/li/a[contains(text(),'%s')]/@href" % (str(i))).get())
                nexts.append(response.xpath("//div/ul/li/a[contains(text(),'%s')]/text()" % (str(i))).get())
        for i, j in zip(nexts, next_cat):
            if i == 'Attachments' or 'Compaction Equipment' or 'Power System Generation':
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
            j = response.xpath("//div/ul/li[@class='category']/a/text()").get()
            used_attachment_path    = "https://www.constructionequipmentguide.com"+ i
            yield scrapy.Request(used_attachment_path, self.parse_item_list,meta={'category':cat_temp,'category2':j})

    def parse_item_list(self, response):
        print("in parse_item_list")
        collection_items = response.xpath("//div[@class='result machine-listing trackImpression']")
        for construct in collection_items:
            default = ""
            item['item_title'] = "".join(collection_items.xpath("//div[@class='machine-model']/a/text()").get()).strip()
            item['item_url']   = "" .join("https://www.constructionequipmentguide.com"+collection_items.xpath("//div[@class='machine-model']/a/@href").get()).strip()
            category1          = response.meta['category'] or default
            category2          = response.meta['category2'] or default
            item['category'] = {'cat1_name': category1,     
                                'cat2_name': category2,
                                'cat1_id': '',
                                'cat2_id': ''
                                }
        next_page = response.xpath(
            "//div/a[@class='button green']/@href").get()
        if next_page is not None:
            next1 = response.urljoin(next_page)
            next_temp = response.xpath("//div/a[@class='button green'][2]/@href").get()
            if next_temp is not None:
                next1 = response.urljoin(next_temp)
            yield scrapy.Request(next1, callback=self.parse_item_list, dont_filter=True,meta={'category':category1,'category2':category2})
        yield item

#

# # from scrapy.cmdline import execute
# # execute("scrapy crawl CGItem".split())
# #

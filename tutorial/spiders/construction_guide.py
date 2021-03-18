import scrapy
from fake_headers import Headers
from tutorial.items import Construction


class ConstructionList(scrapy.Spider):
    name = "CG"
    url = "https://www.constructionequipmentguide.com/"

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse_list_category)

    def parse_list_category(self, response):
        category = response.xpath("//div/ul/li/a/text()").getall()
        item = Construction()
        item['category'] = category
        yield item


class ConstructionItemDetail(scrapy.Spider):
    name = "CGItem"
    url = "https://www.constructionequipmentguide.com/"
    i = 0
    parse_itm = 0
    parse_itm_dtail = 0
    total = {}

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse_item)

    def parse_item(self, response):
        print("in parse_itm", self.parse_itm)
        self.parse_itm += 1
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
        print(next_cat)
        for i, j in zip(nexts, next_cat):
            if i == 'Attachments' or 'Compaction Equipment' or 'Power System Generation':
                next1 = response.urljoin(j)
                yield scrapy.Request(next1,self.used_attachment_item)
            else:
                next1 = response.urljoin(j)
                yield scrapy.Request(next1, self.parse_item_detail)

    def used_attachment_item(self, response):
        print("in used_attachment_item")
        used_attachment = response.xpath(
            "//div/ul/li[@class='category']/a/@href").getall()
        for i in used_attachment:
            used_attachment_path = response.urljoin(i)
            yield scrapy.Request(used_attachment_path, self.parse_item_detail)

    def parse_item_detail(self, response):
        print("parse_itm_dtail", self.parse_itm_dtail)
        self.parse_itm_dtail += 1
        item = Construction()
        item['item_detail'] = response.xpath("//div[@class='machine-model']/a/text()").getall()
        print(item)
        next_page = response.xpath(
            "//div/a[@class='button green']/@href").get()
        print("next_page", next_page)
        if next_page is not None:
            next1 = response.urljoin(next_page)
            next_temp = response.xpath("//div/a[@class='button green'][2]/@href").get()
            if next_temp is not None:
                next1 = response.urljoin(next_temp)
            print("next1", next1)
            yield scrapy.Request(next1, callback=self.parse_item_detail, dont_filter=True)

# from scrapy.cmdline import execute
# execute("scrapy crawl CGItem".split())
#

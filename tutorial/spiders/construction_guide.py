import scrapy
from fake_headers import Headers
from tutorial.items import Construction
import logging
from scrapinghub import ScrapinghubClient
import requests,json,re
from scrapy.http import HtmlResponse




class ConstructionList(scrapy.Spider):
    name = "CG"
    url = "https://www.constructionequipmentguide.com/"

    def start_requests(self):
        yield scrapy.Request(self.url, self.parse_list_category)

    def parse_list_category(self, response):
        item = Construction()
        category = response.xpath("//div/ul[@class='column col1']/li")
        for i in category:
            title       = i.xpath("//a/text()").get()
            item['title'] = title
            category = ''
            item['category'] = {
                    'cat1_name': category,
                    'cat1_id': category,
                    'cat2_name': category,
                    'cat2_id': category
                }
            item['data_id'] = ''
            item['item_custom_info'] = {
                'buying_format': 'Sale',
                'city': '',
                'state': '',
                'country': 'USA'
            }
            yield item


class ConstructionItemDetail(scrapy.Spider):
    name = "CGItem"
    start_urls = ["https://www.constructionequipmentguide.com/"]
    allowed_domains     = ['constructionequipmentguide.com']
    i = 0
    parse_itm = 0
    parse_itm_dtail = 0
    total = {}

    def __init__(self, collection_name=None, *args, **kwargs):
        try:
            super(ConstructionItemDetail, self).__init__(*args, **kwargs)
            global current_collection, additional_information, url, listing_urls, category_names, category_ids, thumb_urls, \
                subcategory_names, subcategory_ids, city, state, country, \
                collection_keys, foo_store, titles, make, model, year, serial_no, item_custom_info

            listing_urls = []
            category_names = []
            category_ids = []
            subcategory_names = []
            subcategory_ids = []
            collection_keys = []
            thumb_urls = []
            city = []
            state = []
            country = []
            titles = []
            make = []
            model = []
            year = []
            serial_no = []
            additional_information = []
            current_collection = ''

        #     apikey = ''
        #     client = ScrapinghubClient(apikey)
        #     project_id = 437850
        #     project = client.get_project(project_id)
        #     collections = project.collections
        #
        #     if not collection_name:
        #         max_number_list = []
        #         max_number_dict = {}
        #         collection_name = [i.get('name') for i in collections.list()]
        #         for k in collection_name:
        #             try:
        #                 get_number = k.split('_')
        #                 number = int(get_number[-1])
        #                 max_number_dict.update({get_number[-1]: k})
        #                 max_number_list.append(number)
        #             except ValueError:
        #                 print("collection name not contain a number!!")
        #
        #         collection_name = max(max_number_list)
        #         collection_name = max_number_dict.get(str(collection_name))
        #         job_run_id = collection_name
        #     else:
        #         job_run_id = collection_name
        #
        #     foo_store = collections.get_store(job_run_id)  # collection_id
        #     print("Getting Items from collection" + str(collection_name))
        #     print("Length of collection" + str(foo_store.count()))
        #     for elem in foo_store.iter():
        #         collection_keys.append(elem['_key'])
        #         listing_urls.append(elem['item_url'])
        #         titles.append(str(elem['title']))
        #         thumb_urls.append(str(elem['thumbnail_url']))
        #     print("Fetched from collection" + str(collection_name))
        except Exception as e:
            logger.error(e)

    def parse(self, response):
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
                yield scrapy.Request(next1,self.used_attachment_item)
            else:
                next1 = response.urljoin(j)
                yield scrapy.Request(next1, self.parse_item_detail)

    def used_attachment_item(self, response):
        used_attachment = response.xpath(
            "//div/ul/li[@class='category']/a/@href").getall()
        for i in used_attachment:
            used_attachment_path = response.urljoin(i)
            yield scrapy.Request(used_attachment_path, self.parse_item_detail)

    def parse_item_detail(self, response):
        item = Construction()
        collection_items = response.xpath("//div[@class='result machine-listing trackImpression']")
        for construct in collection_items:
            default                     = ""
            item['item_title']          = construct.xpath("//div[@class='machine-model']/a/text()").get()
            item['thumbbnail_url']      = construct.xpath("//div[@class='machine-photo']/a/img/@src").get()
            item['thumbnail_s3_path']   = '/thumbnaiimagenotfound.jpg'
            item['city']                = construct.xpath("//div[@class='machine-location']/text()").get().split()[1:]
            item['price_original']      = str(construct.xpath("//div[@class='machine-original-price']/text()").get().split()[2:])
            item['currency']            = "USD"
            item['url']                 = construct.xpath("//div[@class='machine-model']/a/@href").get()
            item['vendor_city']         = item['city']
            item['price']               = construct.xpath("//div[@class='machine-price']/@text()").get()
            try:
                year = item['item_title']
                valid_year = 1900 <= int(re.findall(r'\d{4}', str(year))[0]) <= 2021
                if valid_year is True:
                    year = re.findall(r'\d{4}', str(year))[0]
                    item['year'] = year
            except:
                item['year']         = ""
        next_page = response.xpath(
            "//div/a[@class='button green']/@href").get()
        if next_page is not None:
            next1 = response.urljoin(next_page)
            next_temp = response.xpath("//div/a[@class='button green'][2]/@href").get()
            if next_temp is not None:
                next1 = response.urljoin(next_temp)
            yield scrapy.Request(next1, callback=self.parse_item_detail, dont_filter=True)
        yield item
# from scrapy.cmdline import execute
# execute("scrapy crawl CGItem".split())
#

import scrapy
# from fake_headers import Headers
from tutorial.items import Construction
import logging
from scrapinghub import ScrapinghubClient
import requests,json,re
from scrapy.http import HtmlResponse




class ConstructionList(scrapy.Spider):
    name = "CG"
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
                # item['category'] = {'cat1_name': i,
                #                     'cat2_name': '',
                #                     'cat1_id': '',
                #                     'cat2_id': ''
                #                     }
                yield scrapy.Request(next1, self.used_attachment_item,meta={'category':i})
            else:
                next1 = response.urljoin(j)
                # item['category'] = {'cat1_name': i,
                #                     'cat2_name': '',
                #                     'cat1_id': '',
                #                     'cat2_id': ''
                #                     }
                yield scrapy.Request(next1, self.parse_item_list,meta={'category':i})

    def used_attachment_item(self, response):
        print("in used attachment_item")
        used_attachment = response.xpath(
            "//div/ul/li[@class='category']/a/@href").getall()
        for i in used_attachment:
            cat_temp = response.meta.get("category")
            j = response.xpath("//div/ul/li[@class='category']/a/text()").get()
            used_attachment_path = response.urljoin(i)
            # print(item)
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

            apikey = '3b7e1d959149492ab9a71b9aae0fbff4'
            client = ScrapinghubClient(apikey)
            project_id = 510707
            project = client.get_project(project_id)
            collections = project.collections

            if not collection_name:
                max_number_list = []
                max_number_dict = {}
                collection_name = [i.get('name') for i in collections.list()]
                print(collection_name)
                for k in collection_name:
                    try:
                        get_number = k.split('_')
                        number = int(get_number[-1])
                        max_number_dict.update({get_number[-1]: k})
                        max_number_list.append(number)
                    except ValueError:
                        print("collection name not contain a number!!")

                collection_name = max(max_number_list)
                collection_name = max_number_dict.get(str(collection_name))
                job_run_id = collection_name
            else:
                job_run_id = collection_name

            foo_store = collections.get_store(job_run_id)  # collection_id
            print("Getting Items from collection" + str(collection_name))
            print("Length of collection" + str(foo_store.count()))
            for elem in foo_store.iter():
                collection_keys.append(elem['_key'])
                listing_urls.append(elem['item_url'])
                titles.append(str(elem['title']))
                thumb_urls.append(str(elem['thumbnail_url']))
            print("Fetched from collection" + str(collection_name))
        except Exception as e:
            print(e)

    def parse(self, response):
        def parse(self, response):
            try:
                for i in range(0, len(listing_urls)):
                    yield scrapy.Request(url=listing_urls[i], callback=self.parse_data, meta={
                        'collection_item_key': collection_keys[i],
                        'listing_url': listing_urls[i],
                        'thumb_urls': thumb_urls[i],
                        'titles': titles[i]}, dont_filter=True)
            except Exception as e:
                print(e)


    def parse_item_detail(self, response):
        item = Construction()
        collection_items = response.url
        default                     = ""
        item['item_title']          = response.xpath("//div[@class='equipment-detail']/h1/text()").get()
        item['thumbbnail_url']      = construct.xpath("//div[@class='mySlides']/img/@src").get()
        if 'http' not in item['thumbnail_url']:
            item['thumbnail_url'] = ''
            item['thumbnail_s3_path'] = '/thumbnailimagenotfound.jpg'
        else:
            item['thumbnail_s3_path'] = ''
        categories                          = response.xpath("//span[@itemprop='itemListElement']/span/a/span/text()").getall()
        if categories:
            categories                      = categories[-2:]
        if categories:
            item['item_main_category']      = categories[0]
            item['item_main_category_id']   = categories[0]
            item['category']                = categories[1]
            item['category_id']             = categories[1]
            item['item_sub_category ']      = categories[2]
            item['item_source_sub_category_id'] = categories[2]
        item['buying_format'] = 'Sell'
        price                       = response.xpath("//p[@class='equip-price']/text()").get()
        try:
            price                       = int(eval(price.strip("For Sale:").replace("$", "").replace("USD", "").replace(",", "")))
            item['price']                = price
            if item['price']:
                item['currency']    = 'USD'
        except:
                item['currency']    = item['price'] = ''
        item['price_original']      = item['price']
        item['location']            = response.xpath("//tbody/tr[@class='machine-location']/td[2]").get()
        item['vendor_name']         = 'COnstruction_Equipment_Guide'
        item['vendor_url']          = ""
        item['img_url']             = response.xpath("//div[@class='mySlides']/img/@src").get()
        item['vendor_city'] = ''
        item['vendor_state'] = ''
        item['vendor_country'] = ''
        try:
            year = item['item_title']
            valid_year = 1900 <= int(re.findall(r'\d{4}', str(year))[0]) <= 2021
            if valid_year is True:
                year = re.findall(r'\d{4}', str(year))[0]
                item['year'] = year
        except:
            item['year']         = ""
            item['model']        = ""
            serial_no            = response.xpath("//table//tr[@class='equip-serial']/td[2]").get()
            if serial_no is not None:
                ite['serial_number'] = serial_no
            else:
                item['serial_no']       = ""
        item['auction_ending']          = ""
        item['make']                    = ""
        hours                   = response.xpath("//table[@class='machine-info']/tbody/tr/td[2]").get()
        if hours is not None:
            hours   = {
                'hours':hours
            }
            item['extra_fields']    = hours
        title           = str(response.meta['titles']).replace("null",'')
        item[title]     = title
        next_page = response.xpath(
            "//div/a[@class='button green']/@href").get()
        item['vendor_contact'] = ''
        item['details'] = ''
        if item['item_title'] and item['item_main_category']:
            yield item
        if next_page is not None:
            next1 = response.urljoin(next_page)
            next_temp = response.xpath("//div/a[@class='button green'][2]/@href").get()
            if next_temp is not None:
                next1 = response.urljoin(next_temp)
            yield scrapy.Request(next1, callback=self.parse_item_detail, dont_filter=True)
# # from scrapy.cmdline import execute
# # execute("scrapy crawl CGItem".split())
# #

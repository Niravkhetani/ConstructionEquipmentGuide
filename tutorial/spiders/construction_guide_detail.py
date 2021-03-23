import scrapy
# from fake_headers import Headers
from tutorial.items import Construction
import logging
from scrapinghub import ScrapinghubClient
import requests,json,re
import pandas as pd
from scrapy.http import HtmlResponse



class ConstructionItemDetail(scrapy.Spider):
    name = "ConstructionItemDetail"
    start_urls = ["https://www.constructionequipmentguide.com/"]
    allowed_domains     = ['constructionequipmentguide.com']
    i = 0
    parse_itm = 0
    parse_itm_dtail = 0
    total = {}
    def __init__(self, collection_name=None, *args, **kwargs):
        print("in init")
        try:
            super(ConstructionItemDetail, self).__init__(*args, **kwargs)
            global current_collection, additional_information, url, listing_urls, category_names, category_ids, thumb_urls, \
                subcategory_names, subcategory_ids, city, state, country, \
                collection_keys, foo_store, titles, make, model, year, serial_no, item_custom_info, \
                categories,item_url,item_title,thumbnail_url,cat1

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
            item_title       = []
            item_url        = []
            categories        = []
            cat1            = None

            table = pd.read_csv("tutorial/spiders/newcg.csv")
            item_title = list(table['item_title'])
            item_url = list(table['item_url'])
            thumbnail_url = list(table['thumbbnail_url'])
            categories = str(table['category'])
            print(categories)
            cat1 =  dict((x.strip(), y.strip()) for x, y in (element.split(':') for element in cat2.split(',')))
            # print("cat1", cat1.get('cat1_name'))


            apikey = '3b7e1d959149492ab9a71b9aae0fbff4'
            client = ScrapinghubClient(apikey)
            project_id = 511126
            project = client.get_project(project_id)
            # collections = project.collections

            # if not collection_name:
            #     max_number_list = []
            #     max_number_dict = {}
            #     collection_name = [i.get('name') for i in collections.list()]
            #     print(collection_name)
            #     for k in collection_name:
            #         try:
            #             get_number = k.split('_')
            #             number = int(get_number[-1])
            #             max_number_dict.update({get_number[-1]: k})
            #             max_number_list.append(number)
            #         except ValueError:
            #             print("collection name not contain a number!!")
            #
            #     collection_name = max(max_number_list)
            #     collection_name = max_number_dict.get(str(collection_name))
            #     job_run_id = collection_name
            # else:
            #     job_run_id = collection_name

            # foo_store = collections.get_store(job_run_id)  # collection_id
        #     print("Getting Items from collection" + str(collection_name))
        #     print("Length of collection" + str(foo_store.count()))
        #     for elem in foo_store.iter():
        #         collection_keys.append(elem['_key'])
        #         listing_urls.append(elem['item_url'])
        #         titles.append(str(elem['title']))
        #         thumb_urls.append(str(elem['thumbnail_url']))
        #     print("Fetched from collection" + str(collection_name))
        except Exception as e:
            print(e)



    def parse(self, response):
        try:
            for i in range(0, len(item_url)):
                yield scrapy.Request(url=item_url[i], callback=self.parse_item_detail, meta={
                    'listing_url': item_url[i],
                    'titles': item_title[i]}, dont_filter=True)
        except Exception as e:
            print(e)
    #
    #
    def parse_item_detail(self, response):
        item = Construction()
        collection_items = response.url
        default                     = ""
        item['item_title']          = response.xpath("//div[@class='equipment-detail']/h1/text()").get()
        item['thumbbnail_url']      =  thumbnail_url
        if 'http' not in item['thumbbnail_url']:
            item['thumbbnail_url'] = ''
            item['thumbnail_s3_path'] = '/thumbnailimagenotfound.jpg'
        else:
            item['thumbnail_s3_path'] = ''
        item['img_url']             = response.xpath("//div[@class='mySlides']/img/@src").get()
        if categories:
            item['item_main_category']      = categor[0]
            item['item_main_category_id']   = categor[0]
            item['category']                = categor[1]
            item['category_id']             = categor[1]
        location            = response.xpath("//table[@class='machine-info']//tr[@class='machine-location']/td[2]").get()
        if location is not None:
            item['location']    = location
            item['vendor_location'] = location
            item['extra_fields'] = {
                'location':location,
                'vendor_location':location
            }
        else:
            item['location']    = ""
        thumbnai_url            = response.xpath("//img[@class='demo cursor']/@src").getall()
        if thumbnai_url:
            item['thumbbnail_url'] = thumbnai_url
        else:
            item['thumbbnail_url']      = ""
        item['vendor_contact']          = ""
        make                    = response.xpath("//div[@class='breadcrumbs']//span[@content='2']//span/text()").get()
        item['make']            = make
        model                   = response.xpath("//div[@class='breadcrumbs']//span[@content='4']//span/text()").get()
        item['model']           = model
        item['url']             = response.url
        item['buying_format'] = 'Sale'
        price                       = response.xpath("//p[@class='equip-price']/text()").get()
        try:
            price                       = int(eval(price.strip("For Sale:").replace("$", "").replace("USD", "").replace(",", "")))
            item['price']                = price
            if item['price']:
                item['currency']    = 'USD'
        except:
                item['currency']    = item['price'] = ''
        item['price_original']      = item['price']
        vendor_name                 = response.xpath("//div[@class='dealer-name']/h4/text()").get()
        if vendor_name:
            item['vendor_name']         = 'COnstruction_Equipment_Guide'
        else:
            item['vendor_name']         = ""
        vendor_url                  = response.xpath("//div[@class='more-info']/a/@href").get()
        if vendor_url:
            item['vendor_url']      = vendor_url
        else:
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
                item['serial_number'] = serial_no
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
        else:
            item['extra_fields']    = ""
        title           = str(response.meta['titles']).replace("null",'')
        item['title']     = title
        next_page = response.xpath(
            "//div/a[@class='button green']/@href").get()
        item['vendor_contact'] = ''
        item['details'] = ''
        yield item
        # if item['item_title'] and item['item_main_category']:

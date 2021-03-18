# import scrapy

# class ScrapyQuote(scrapy.Spider):
#     name        = "walk"
    # start_urls  = [
    #     "http://quotes.toscrape.com",
    # ]

    # def parse(self,response):
    #     author_page         = response.css(".author + a")
    #     yield from response.follow_all(author_page,self.parse_all)

    #     next                = response.css("li.next  a")
    #     print("next",next)
    #     yield from response.follow_all(next,self.parse)
    
    # def parse_all(self,response):
    #     def catch_css(query):
    #         return response.css(query).get(default="")
        
    #     yield {
    #         'author':catch_css("h3.author-title::text"),
    #         'born':catch_css("span.author-born-date::text"),
    #         'desc':catch_css("div.author-description::text")
    #     }

    # def start_requests(self):
    #     url         = 'http://quotes.toscrape.com/'
    #     tag         = getattr(self,'tag',None)
    #     if tag is not None:
    #         url     = url + 'tag/' + tag
    #     yield scrapy.Request(url,self.parse)

    # def parse(self,response):
    #     for quote in response.css("div.quote"):
    #         yield {
    #             'quote':quote.css("span.text::text").get(),
    #             'author':quote.css("small.author::text").get()
    #         }
    #     next        = response.css("li.next a")
    #     yield from response.follow_all(next,self.parse)



    # start_urls  = [
    #     "http://quotes.toscrape.com/"
    # ]

    # def parse(self,response):
    #     author      = response.css("small.author::text").getall()
    #     text        = response.css("div.quote::attr(itemtype)").getall()
    #     yield {
    #         'author':author,
    #         'text':text
    #     }


from scrapy.spiders import XMLFeedSpider,CSVFeedSpider
from tutorial.items import TutorialItem
import scrapy


# class MySpider(CSVFeedSpider):
#     name = 'example.com'
#     # allowed_domains = ['quotes.toscrape.com']
#     start_urls = ['http://quotes.toscrape.com/']
#     custom_settings = {"FEEDS":{"new.csv":{"format":"csv"}}}
#     delimiter  = ';'
#     quotechar  = "'"
#     header     = ['quote','author']

#     def parse_row(self, response, row):
#         self.logger.info('Hi, this is row',row)

#         item = TutorialItem()
#         # item['id'] = node.xpath('@id').get()
#         item['quote'] = response.css("div.quote span.text::text").get()
#         item['author'] = response.css("small.author::text").get()
#         # item['description'] = node.xpath('description').get()
#         return item
# from scrapy.cmdline import execute
# execute("scrapy crawl walkthrough".split())

# from scrapy.loader import ItemLoader

# class ItemLoaderSpider(scrapy.Spider):
#     name        = "ItemLoad"
#     start_urls  = ["http://quotes.toscrape.com/"]

#     def parse(self,response):
#         t1      = ItemLoader(item=TutorialItem(),response=response)
#         print("t1",t1)
#         t1.add_xpath('quote','//div[@class="quote"]/span//text()').get()
#         t1.add_xpath('author','//small[@class="author"]//text()').get()
#         return t1.load_item()

# from scrapy.http import FormRequest



# # class LoginTuto(scrapy.Spider):
# #     name='logintu'
# #     def start_requests(self):
# #         url = "http://quotes.toscrape.com/login"
# #         return [
# #             FormRequest(url,formdata={'username':"admin",'password':'admin'},
# #             callback=self.parse)    
# #         ]
# #     def parse(self,response):
# #         return response.xpath("//a/@href").get()
        

# import scrapy
# from scrapy.http import FormRequest
# import json
# from scrapy.selector import Selector
# # class LoginSpider(scrapy.Spider):
# #     name = 'login'
# #     allowed_domains = ['quotes.toscrape.com']
# #     start_urls = ['http://quotes.toscrape.com/login']
# #     def parse(self,response):
# #             csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
# #             return FormRequest.from_response(response, formdata={'csrf_token': csrf_token, 'user':'user', 'pass':'pass'}, callback=self.parse_after_login)
# #     def parse_after_login(self,response):
# #         return response.xpath("//a/@href").get()
import json
from tutorial.items import TutorialItem
# class JsonSpider(scrapy.Spider):
#     name        = 'purplewave'
    
#     def start_requests(self):
#         urls     = [
#             'https://www.purplewave.com/v1/search/search?searchType=all&dateType=upcoming&dateRanges=&auctions=210317&zipcode=&zipcodeRange=all&startPrice=0&endPrice=0&filters=family_category_id%3A624&showDefault=false&isOnSaleOrder=false&sortBy=current_bid-desc&page=1&perPage=50&viewtype=compressed&auctionId=210317&returnFields=compressed&grouped=false&timestamp=0&_=1615533553&return_fields=auction%2Ctitle%2Cdescription%2Citem%2Ccity%2Cstate_abbreviation%2Cstate_name%2Cimage%2Cimage_url%2Cpostal_code%2Cfirst_line_description%2Cfamily_category%2Ccategory%2Cmake%2Cmodel%2Cyear%2Cthumbnail%2Cnum_images%2ClastLoginTime%2Cdate_created%2Cclosed%2Chalted%2Chalted_message%2Ccurrent_bid%2Cworkspace%2Cicn%2Cbid_count%2Cnext_bid%2Cmaxbid%2Cid%2Ccontract_price%2Cwinning_bidder%2Cseller_alt%2Centities%2Cvideo_hd_url%2Cgroup%2Clocation_simLink_thisAuction%2Cnid%2Cendtime%2Cextended%2Cclosing%2Csortorder%2Csortgroups%2Cauction_time%2Cauction_timestamp%2Cauction_closing%2Cauction_endtime%2Cendtime%2Cauction_closed%2Csold%2Cunique_bidders%2Cprivate_bidders'
#                     ]
#         for url in urls:
#             yield scrapy.Request(url,callback=self.parse)

#     def parse(self,response):
#         i       = json.loads(response.text)
#         # print(i.get('description'))
#         # print("i",i)
#         for j in i:
#             # print(j['first_line_description'])
#             item = TutorialItem()
#             # print(j)
#             item['author'] = j['first_line_description']
#             item['city']   = j['city']
#             yield item
            
            # if(j=='first_line_description'):
            #     print(j,dict(j))

        # s       = Selector(i.get('first_line_description'))
        # print(type(s))
        # print(s.xpath("//b/text()").get())

# from scrapy.utils.response import open_in_browser
# class SearchSpider(scrapy.Spider):

#     name = 'search'
#     # def start_requests(self):
    
        

        
#         urls = "http://quotes.toscrape.com/login"
#         return [
#             FormRequest(urls,formdata={'username':'admin','password':'admin'},callback=self.parse_after)
#         ]
    
#     # def parse(self,response):
#     #     return FormRequest.from_response(response,formdata={'searchTerm': 'truck'}, callback=self.parse_after)

#     def parse_after(self,response):
#         open_in_browser(response)
#         # yield {
#         #     'success': response.xpath('//div/p/a//text()').get()
#         # }
#         # yield json.dumps(response.Text)
     
# import json
# class PurpleWave(scrapy.Spider):
    
#     name        = 'title'

#     def start_requests(self):
#         url     = [ 'https://www.purplewave.com/v1/search/search?searchType=all&dateType=upcoming&dateRanges=&auctions=210317&zipcode=&zipcodeRange=all&startPrice=0&endPrice=0&filters=family_category_id%3A624&showDefault=false&isOnSaleOrder=false&sortBy=current_bid-desc&page=1&perPage=50&viewtype=compressed&auctionId=210317&returnFields=compressed&grouped=false&timestamp=0&_=1615531208&return_fields=auction%2Ctitle%2Cdescription%2Citem%2Ccity%2Cstate_abbreviation%2Cstate_name%2Cimage%2Cimage_url%2Cpostal_code%2Cfirst_line_description%2Cfamily_category%2Ccategory%2Cmake%2Cmodel%2Cyear%2Cthumbnail%2Cnum_images%2ClastLoginTime%2Cdate_created%2Cclosed%2Chalted%2Chalted_message%2Ccurrent_bid%2Cworkspace%2Cicn%2Cbid_count%2Cnext_bid%2Cmaxbid%2Cid%2Ccontract_price%2Cwinning_bidder%2Cseller_alt%2Centities%2Cvideo_hd_url%2Cgroup%2Clocation_simLink_thisAuction%2Cnid%2Cendtime%2Cextended%2Cclosing%2Csortorder%2Csortgroups%2Cauction_time%2Cauction_timestamp%2Cauction_closing%2Cauction_endtime%2Cendtime%2Cauction_closed%2Csold%2Cunique_bidders%2Cprivate_bidders' ]
#         for u in url:
#             yield scrapy.Request(u,callback=self.parse)

#     def parse(self,response):
#         text = json.loads(response.text)
#         for i in text:
#             print(j['first_line_description'])
#         yield text

from scrapy.selector import Selector

# class Ironlistdata(scrapy.Spider):
#     name        = 'ironlist'

#     def start_requests(self):
#         url     = "https://www.ironlist.com/listing?keyword=&search=%3Ekeyword%3D%2C&searchLocation=&format=Auction"
#         yield scrapy.Request(url,callback=self.parse)


#     def parse(self,response):
#         # print(response.text)
#         data    = Selector(response)
#         item    = TutorialItem()
#         # print(data)
#         item['title'] = data.xpath("//h3[@class='text-black truncate cursor-pointer w-card-heading sm:w-full xl:max-w-xsm laptop:max-w-lg laptopM:max-w-lg text-mobile-heading lg:text-base xl:text-xl laptop:text-2xl font-semibold']/a/text()").get()
#         item['class_type'] = data.xpath("//p[@class='text-black text-mobile-text lg:text-base xl:text-lg opacity-90 mb-1 lg:mb-1']/text()").get()
#         item['cmp_name'] = data.xpath("//p[@class='text-black flex items-center text-mobile-text lg:text-base xl:text-xl font-medium mb-1 lg:mb-2']/text()").get()
#         item['location'] = data.xpath("//p[@class='text-mobile-text truncate lg:max-w-xxxs laptop:max-w-xs lg:text-xs xl:text-base w-4/5 lg:w-auto xl:text-lg opacity-90']/text()").get()
#         yield item


# class Rbdata(scrapy.Spider):
#     name    = 'rbauction'
#     def start_requests(self):
#         urls = [ "https://www.craneequipmentguide.com/equipment/used-boom-truck-cranes-for-sale/" ]
        
#         for url in urls:
#             yield scrapy.Request(url,callback=self.parse)

#     def parse(self,response):
#         title       = response.xpath('//div[@class="machine-ymm"]/text()').getall()
#         for i in title:
#             print(str(i).strip().strip("\t").strip("\n"))
#         item        = TutorialItem()
#         item['title'] = title
#         # next        = response.xpath('//div[@class="buttons-php"]/a[contains(@rel,"next")]/@href').get()
#         next        = response.xpath("//div[@class='buttons-php']/a")
#         print("next",next)
#         yield from response.follow_all(next,self.parse)
        # next_count  = next.split('/')
        # print("next_count",next_count)
        # if next is not None:
        #     next_page = response.urljoin(next)
        #     yield scrapy.Request(next_page,self.parse)

from scrapy.http import FormRequest

class Rdodata(scrapy.Spider):
    
    name        = 'rdoequip'

    def start_requests(self):
        url     = 'https://www.rdoequipment.com/equipment/used'
        
        formdata = json.dumps({'hitsPerPage': 10,
                    'maxValuesPerFacet': 100,
                    'page': 0})
        headers  = json.dumps({
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US, en",
            "Connection": "keep-alive",
            "Content-Length": "303",
            "content-type": "application/x-www-form-urlencoded",
            "Host": "smdbeujv3e-1.algolianet.com",
            "Origin": "https: // www.rdoequipment.com",
            "Referer": "https: // www.rdoequipment.com /",
            "sec-ch-ua": "Google Chrome",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0 Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        })                   
        yield FormRequest(url,formdata=formdata,headers=headers,callback=self.parse)


    def parse(self,response):
        print(response)
        yield response
    
    def parse_all(self):
        pass



        

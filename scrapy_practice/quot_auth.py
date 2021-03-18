# import scrapy


# class Spider2(scrapy.Spider):
#     name        = "quot3"

#     start_urls  = [
#         "http://quotes.toscrape.com/"
#     ]

#     def parse(self,response):
#         for quote in response.css("div.quote"):
#             yield {
#             'quot'        : quote.css("span.text::text").get(),
#             'author'      : quote.css("small.author::text").get(),
#             'tags'        : quote.css("div.tags a.tag::text").getall()
#         }
#         # next_page       = response.css("li.next a::attr(href)").get()
#         next_page        = response.css("ul.pager a")
#         yield from response.follow_all(next_page,callback=self.parse)
#         # print(next_page)
#         # if next_page is not None:
#         #     # next_page   = response.urljoin(next_page)
#         #     # yield scrapy.Request(next_page,callback=self.parse)
#         #     yield scrapy.follow(next_page,callaback=self.parse)


import scrapy


class Auth_det(scrapy.Spider):
    name            = "auth_detail"

    start_urls      = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self,response):
        auth        = response.css(".author + a")
        yield from response.follow_all(auth,self.parse_author)

        next_link   = response.css("li.next a")
        yield from response.follow_all(next_link,self.parse)

    
    def parse_author(self,response):
        
        def extract_with_css(query):
            # print("response.css(query).get(default='').strip()",
            #       response.css(query).get(default='').strip())
            return response.css(query).get(default='').strip()
        
        yield   {
            'name': extract_with_css("h3.author-title::text"),
            'born': extract_with_css(".author-born-date::text"),
            'desc': extract_with_css(".author-description::text")
        }

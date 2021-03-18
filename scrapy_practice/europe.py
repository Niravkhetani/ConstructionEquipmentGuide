import scrapy
from tutorial.items import TutorialItem
from fake_headers import Headers
from tutorial.pipelines import DatabasePipeline

class Ecs(scrapy.Spider):
    name    = "ECS"
    i = 1
    par = 1
    req = 1
    ite = 1
    url     = 'https://www.europe-construction-equipment.com/'
    def start_requests(self):
        header = Headers(
            browser="chrome",  # Generate only Chrome UA
            os="win",  # Generate ony Windows platform
            headers=True  # generate misc headers
        )
        header1=None
        for i in range(10):
            header1 = header.generate()
        print('in start requests' , "     ",self.req)
        self.req        = self.req+1
        # headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        yield scrapy.Request(self.url, self.parse, headers=header1)

    
    def parse(self,response):
        header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
        header1=None

        for i in range(10):
            header1 = header.generate()
        print("in parse" , "   ",self.par)
        self.par     = self.par+1
        item_page    = response.xpath("//div[@class='row']/a")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        yield from response.follow_all(item_page, self.parse_item, headers=header1)

    def parse_item(self,response):
        # if __name__ == "__main__":
        header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
        header1=None
        for i in range(10):
            header1=header.generate()
        print(header1)
        print(header1)
        print("in parse_item")
        item_detail   = response.xpath("//div[@class='row-listing  page-break-inside  ']/div/@data-ihref").get()
        if item_detail is not None:
            print(item_detail  ," ",self.i)
            self.i=self.i+1
            url       = response.urljoin(item_detail)
            # headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
            yield scrapy.Request(url, self.parse_item_detail, headers=header1)
        next = response.xpath(
            "//div[@class='flex-row width-pct-100 flex-12']/a/@data-href").get()
        if next is not None:
            print("in next is not None")
            next_temp=response.xpath(
                "//div[@class='flex-row width-pct-100 flex-12']/a[2]/@data-href").get()
            if next_temp is not None:
                next    = next_temp
        print("next", next)
        if next is not None:
            next_page   = response.urljoin(next)
            yield scrapy.Request(next_page,self.parse_item,headers=header1)
            yield from response.follow_all(next, self.parse_item)

    def parse_item_detail(self,response):
        header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )

        # for i in range(10):
        #     print(header.generate())
        print("in parse_item_detail " , "     ",self.ite)
        self.ite = self.ite+1
        title_temp          = str(response.xpath("//h1[@class='padding-0 margin-0 padding-top-5 title-ts']/text()").get())
        title               = title_temp.strip().strip("\n")
        item                = TutorialItem()
        item['title']       = title
        # db, user, passwd, host = "scrapy_ecs","root","","127.0.0.1"
        # d1                  = DatabasePipeline(db,user,passwd,host)
        # d1.open_spider(ECS)
        # d1.process_item(item,ECS)
        # d1.close_spider(ECS)
        yield item
    

    
# from scrapy.cmdline import execute
# execute("scrapy crawl europe".split()) 




import scrapy
from scrapy.selector import Selector

class ncmachine(scrapy.Spider):
    name        = 'ncmachinery'

    urls  = 'https://www.ncmachinery.com/cat_used_equipments/search?utf8=%E2%9C%93&manufacturer_search=&product_family=&model=&serial_number=&unit_number=&year_start=&year_end=&price_start=&price_end=&hours_start=&hours_end=&submit=Submit'

    def start_requests(self):
        yield scrapy.Request(self.urls,self.parse)

    def parse(self,response):
        data    = response.xpath("//tbody")
        for pro in data:
            # print(pro)
            print(pro.xpath("//tr/td[3]/text()").getall())
            print(pro.xpath("//tr/td[4]/text()").getall())
        print(type(data))
        # print(data)
        # print(data.strip().strip("\n"))
        # data        = list(map(str.strip,data))
        # print(data)
        next    = response.xpath("//a[@class='next_page']")
        if next is not None:
            yield from response.follow_all(next,self.parse)


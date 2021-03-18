# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # Id = scrapy.Field()
    title = scrapy.Field()
    # class_type = scrapy.Field()
    # cmp_name = scrapy.Field()
    # location = scrapy.Field()
    # pass

class Construction(scrapy.Item):
    category        = scrapy.Field()
    item_detail     = scrapy.Field()

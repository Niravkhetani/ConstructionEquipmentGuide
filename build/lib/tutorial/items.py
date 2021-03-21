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
    category                    = scrapy.Field()
    item_detail                 = scrapy.Field()
    title                       = scrapy.Field()
    data_id                     = scrapy.Field()
    item_custom_info            = scrapy.Field()
    item_main_category          = scrapy.Field()
    item_main_category_id       = scrapy.Field()
    item_category               = scrapy.Field()
    item_category_id            = scrapy.Field()
    item_source_sub_category_id = scrapy.Field()
    item_sub_category           = scrapy.Field()
    vendor_url                  = scrapy.Field()
    item_url                    = scrapy.Field()
    make                        = scrapy.Field()
    model                       = scrapy.Field()
    year                        = scrapy.Field()
    price_original              = scrapy.Field()
    currency                    = scrapy.Field()
    extra_fields                = scrapy.Field()
    serial_number               = scrapy.Field()
    thumbbnail_url              = scrapy.Field()
    thumbnail_s3_path           = scrapy.Field()
    item_title                  = scrapy.Field()
    city                        = scrapy.Field()
    url                         = scrapy.Field()
    price                       = scrapy.Field()
    vendor_city                 = scrapy.Field()
    vendor_state                = scrapy.Field()
    vendor_name                 = scrapy.Field()
    vendor_location             = scrapy.Field()
    vendor_contact              = scrapy.Field()
    source_item_id              = scrapy.Field()
    auction_ending              = scrapy.Field()
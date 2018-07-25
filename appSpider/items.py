# -*- coding: utf-8 -*-
import scrapy


class AppspiderItem(scrapy.Item):
    app_id = scrapy.Field()
    charge = scrapy.Field()
    name = scrapy.Field()
    developer = scrapy.Field()
    category = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    updated = scrapy.Field()
    size = scrapy.Field()
    installs = scrapy.Field()
    version = scrapy.Field()
    new = scrapy.Field()
    num_comments = scrapy.Field()
    rate_1 = scrapy.Field()
    rate_2 = scrapy.Field()
    rate_3 = scrapy.Field()
    rate_4 = scrapy.Field()
    rate_5 = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()


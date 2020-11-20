import scrapy


class FundascrapItem(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    city = scrapy.Field()
    buurt = scrapy.Field()
    subtitle = scrapy.Field()
    price = scrapy.Field()
    area1 = scrapy.Field()
    area2 = scrapy.Field()
    rooms = scrapy.Field()
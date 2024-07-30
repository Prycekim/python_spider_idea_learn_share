# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ShopeeRemarkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #交易号
    orderid = scrapy.Field()
    #商品号
    itemid = scrapy.Field()
    #用户号
    userid = scrapy.Field()
    #店铺号
    shopid = scrapy.Field()
    #星级
    rating_star = scrapy.Field()
    #用户名
    author_username = scrapy.Field()
    #商品名字
    product_items_name = scrapy.Field()
    #商品图片
    product_items_image = scrapy.Field()
    #客户主观评价
    user_comment = scrapy.Field()
    #商家回复
    Merchant_response = scrapy.Field()
    #地区
    region = scrapy.Field()

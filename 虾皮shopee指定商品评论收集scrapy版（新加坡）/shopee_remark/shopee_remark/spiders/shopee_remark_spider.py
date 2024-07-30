import scrapy
import json
from ..items import ShopeeRemarkItem



class ShopeeRemarkSpiderSpider(scrapy.Spider):
    name = "shopee_remark_spider"
    allowed_domains = ["shopee.sg"]
    start_urls = ["https://shopee.sg/api/v2/item/get_ratings?exclude_filter=1&filter=0&filter_size=0&flag=1&fold_filter=0&itemid=22657061517&limit=6&offset=6&relevant_reviews=false&request_source=2&shopid=1006220784&tag_filter=&type=0&variation_filters="]

    offset = 6
    def parse(self, response):
        #提取字典
        items = ShopeeRemarkItem()
        #拿到请求结果转json
        res = json.loads(response.text)
        # print(res)
        #拿到评论部分，遍历每个人的评论，输送到item
        res_lst = res['data']['ratings']
        for res_target in res_lst:
            #交易号
            items['orderid'] = res_target['orderid']
            # print(items['orderid'])
            #商品号
            items['itemid'] = res_target['itemid']
            # print(items['itemid'])
            #用户号
            items['userid'] = res_target['userid']
            # print(items['userid'])
            #店铺号
            items['shopid'] = res_target['shopid']
            # print(items['shopid'])
            #星级
            items['rating_star'] = res_target['rating_star']
            # print(items['rating_star'])
            #用户名
            items['author_username'] = res_target['author_username']
            # print(items['author_username'])
            #商品名字
            items['product_items_name'] = res_target['product_items'][0]['name']
            # print(items['product_items_name'])
            ##商品图片
            items['product_items_image'] = res_target['product_items'][0]['image']
            # print(items['product_items_image'])
            #客户主观评价
            items['user_comment'] = res_target['comment']
            # print(items['user_comment'])
            #商家回复
            if 'ItemRatingReply' in res_target and 'comment' in res_target['ItemRatingReply']:
                items['Merchant_response'] = res_target['ItemRatingReply']['comment']
            else:
                items['Merchant_response'] = '无'
            # print(items['Merchant_response'])
            #地区
            items['region'] = res_target['region']
            # print(items['region'])
            yield items
 
        if self.offset < 300:
            self.offset += 6
            url = 'https://shopee.sg/api/v2/item/get_ratings?exclude_filter=1&filter=0&filter_size=0&flag=1&fold_filter=0&itemid=22657061517&limit=6&offset={}&relevant_reviews=false&request_source=2&shopid=1006220784&tag_filter=&type=0&variation_filters='\
            .format(str(self.offset))
 
            yield scrapy.Request(url=url,callback=self.parse)
            
                
    
            

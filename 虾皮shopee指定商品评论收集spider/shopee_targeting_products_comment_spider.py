import requests
import re
import time
import random
from ua_info import ua_list
import pandas as pd
import json
import os

# 定义一个spider类
class shopee_Spider: 
    # 初始化
    # 定义初始页面url
    def __init__(self,shop_id,product_id,page_num,input_type):
        self.url = 'https://shopee.tw/api/v2/item/get_ratings?exclude_filter=1&filter=0&filter_size=0&flag=1&fold_filter=0&itemid={}&limit=6&offset={}&relevant_reviews=false&request_source=2&shopid={}&tag_filter=&type={}&variation_filters='
        #店铺id
        self.shop_id = shop_id
        #用户选择的商品id
        self.product_id = product_id
        #用户要获取的页数
        self.page_num = page_num
        #用户选择的评论类型
        self.input_type = input_type
        #存储文件名
        self.file_name = 'shopee_remarks.csv'
        #提前创建好空的csv文件用于存储
        if not os.path.exists(self.file_name):
            df = pd.DataFrame(columns=['交易号', '商品号', '用户号', '店铺号', '星级','用户名','商品名字','商品图片','客户主观评价','商家回复','地区'])
            df.to_csv(self.file_name, index=False, encoding='utf-8-sig')         



    # 请求函数
    def get_response(self,url):
        headers = {'User-Agent':random.choice(ua_list)}
        response = requests.get(url, headers=headers,verify=False)
        if response.status_code == 200:
            data = json.loads(response.text)
            self.parse_response(data)
        else:
            print("请求失败，状态码：", response.status_code)
            return response.status_code
        
        
        
    # 解析函数---JSON---数据存储进csv
    def parse_response(self,response_data):
        #创建一个空的容器
        shopee_data = []
        #提取评论中需要的部分
        res_lst = response_data['data']['ratings']
        #循环遍历
        for res_target in res_lst:
            #交易号
            orderid = res_target['orderid']
            #商品号
            itemid = res_target['itemid']
            #用户号
            userid = res_target['userid']
            #店铺号
            shopid = res_target['shopid']
            #星级
            rating_star = res_target['rating_star']
            #用户名
            author_username = res_target['author_username']
            #商品名字
            product_items_name = res_target['product_items'][0]['name']
            ##商品图片
            product_items_image= res_target['product_items'][0]['image']
            #客户主观评价
            user_comment = res_target['comment']
            #商家回复
            if 'ItemRatingReply' in res_target and 'comment' in res_target['ItemRatingReply']:
                Merchant_response = res_target['ItemRatingReply']['comment']
            else:
                Merchant_response = '无'
            #地区
            region= res_target['region']
            
            shopee_data.append([orderid, itemid,  userid, shopid,rating_star,author_username,product_items_name,product_items_image,user_comment,Merchant_response,region])
            
            
        new_data = pd.DataFrame(shopee_data, columns=['交易号', '商品号', '用户号', '店铺号', '星级','用户名','商品名字','商品图片','客户主观评价','商家回复','地区'])
        
        print(new_data)
        
        self.save_data(new_data) 

    #存储函数
    def save_data(self,new_data):
        new_data.to_csv(self.file_name, mode='a', index=False, header=False, encoding='utf-8-sig')
        


    # 主函数
    def run(self):
        offset = 0
        #个悲剧用户输入参数拼接url
        for self.page in  range(1, self.page_num + 1):
            offset = offset + 6
            #拼接生成url
            print(offset)
            if self.input_type in {'0','1','2','3','4','5'}:
                url = self.url.format(str(self.product_id),str(offset),str(self.shop_id),str(self.input_type))
            else:
                return print('请选择类型')
            print(url)
            #启动请求函数
            self.get_response(url)
            time.sleep(1)
            
        print('执行完毕')




# 以脚本方式启动
if __name__ == '__main__':
    # 使用正则表达式提取商品ID
    print("给我一个商品地址")
    product_id_url = input()
    print('\n选择要获取的评论类型(输入对应编码,如：选择五颗星就输入5):\n###########\n#全部评论:        0\n##五颗星:         5\n##四颗星:         4\n##三颗星:         3\n##两颗星:         2\n##一颗星:         1\n')
    input_type = input()
    print("输入您想要获取几页评论:")
    page_num = input()
    product_pattern = r"i\.\d+\.(.*?)\?sp_atk"
    shop_pattern = r"i\.(.*?)\."
    shop_match = re.search(shop_pattern, product_id_url)
    product_match = re.search(product_pattern, product_id_url)
    if shop_match and product_match:
        shop_id = shop_match.group(1)
        product_id = product_match.group(1)
        print("商品id是:" + product_id )
        print("店铺id是:" + shop_id )
        print("------即将获取-----" + page_num+"页------")
        print("准备启动!")
        time.sleep(2)
    elif shop_match is None:
        print("没有找到店铺id,确认商品链接是否正确,若确认商品链接没有问题,请联系管理员或开发人员！！！")
        time.sleep(10)
    elif product_match is None:
        print("没有找到商品id,确认商品链接是否正确,若确认商品链接没有问题,请联系管理员或开发人员！！！")
        time.sleep(10)
    try:
        #传参：id/页数，然后启动爬虫
        spider = shopee_Spider(shop_id,product_id,int(page_num),str(input_type))
        spider.run()
    except Exception as e:
        print("错误:",e)

    print('程序执行完毕')


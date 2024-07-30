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
    def __init__(self,page_num):
        self.url = 'https://my.lazada.com.my/pdp/review/getReviewList?itemId=4070686268&pageSize=5&filter=0&sort=0&pageNo={}'
        #用户要获取的页数
        self.page_num = page_num




    # 请求函数
    def get_response(self,url):
        headers = {'User-Agent':random.choice(ua_list)}
        response = requests.get(url, headers=headers,verify=False)
        if response.status_code == 200:
            try:
                data = json.loads(response.text)
                self.parse_response(data)
            except:
                print(response.text)
        else:
            print("请求失败，状态码：", response.status_code)
            return response.status_code
        
        
        
    # 解析函数---JSON---数据存储进csv
    def parse_response(self,response_data):
        #创建一个空的容器
        lazada_data = []
        #提取评论中需要的部分
        res_lst = response_data['model']['items']
        #循环遍历
        for res_target in res_lst:
            images_lst = []
            
            #itemsid
            itemId = res_target['itemId']
            #评论类型
            reviewType = res_target['reviewType']
            #购买时间
            boughtDate = res_target['boughtDate']
            #状态
            reviewStatus = res_target['reviewStatus']
            #评论内容
            reviewContent = res_target['reviewContent']
            #评论时间
            reviewTime = res_target['reviewTime']
            #图片
            for i in res_target['images']:
                images_lst.append(i['url'])
            
            images = images_lst
            #买家id
            buyerId = res_target['buyerId']
            #买家名字
            buyerName = res_target['buyerName']
            #skuid
            skuId = res_target['skuId']
            #sku信息
            skuInfo = res_target['skuInfo']
            #等级
            rating = res_target['rating']
            
            lazada_data.append([itemId, reviewType,  boughtDate, reviewStatus,reviewContent,reviewTime,images,buyerId,buyerName,skuId,skuInfo,rating])
            
            
        new_data = pd.DataFrame(lazada_data, columns=['itemsid', '评论类型', '购买时间', '状态', '评论内容','评论时间','图片','买家id','买家名字','skuid','sku信息','等级'])
        
        print(new_data)
        
        self.save_data(new_data) 

    #存储函数
    def save_data(self,new_data):
        print(new_data)
        


    # 主函数
    def run(self):
        page_num = 0
        #拼接页数
        for self.page in  range(1, self.page_num + 1):
            page_num = page_num + 1
            #拼接生成url
            print(page_num)
            url = self.url.format(str(page_num))
            print(url)
            #启动请求函数
            self.get_response(url)
            time.sleep(1)
            
        print('执行完毕')




# 以脚本方式启动
if __name__ == '__main__':
    print("输入您想要获取几页评论:")
    page_num = input()
    try:
        #传参：id/页数，然后启动爬虫
        spider = shopee_Spider(int(page_num))
        spider.run()
    except Exception as e:
        print("错误:",e)

    print('程序执行完毕')

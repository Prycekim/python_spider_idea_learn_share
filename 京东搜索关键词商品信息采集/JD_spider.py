import requests, json
from bs4 import BeautifulSoup
import os
import pandas as pd
import time

# 父类
class OBJECT_JD:
    def __init__(self, cookie, use_cookie=True):
        if use_cookie:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36',
                'cookie': cookie}
        else:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36'
            }
        self.sess = requests.session()
        self.sess.headers.update(self.headers)
        self.file_name = 'jd_product.csv'
        # Check if file already exists, if not create it and write the header
        if not os.path.exists(self.file_name):
            df = pd.DataFrame(columns=[
                'sku', '图片', '价格', '商品标题', '评论数',
                '评论链接', '店铺名', '店铺链接','地区'
            ])
            df.to_csv(self.file_name, index=False, encoding='utf-8-sig')    


# spider类
class Spider(OBJECT_JD):
    def __init__(self, cookie, keyword, end_page):
        super(Spider, self).__init__(cookie)
        self.keyword = keyword
        self.end_page = end_page
        self.start_url = 'https://search.jd.com/Search?keyword=' + keyword + '&enc=utf-8&pvid=d6748e8118e14fd8afae40867d7d52f9'


    def get_item_info(self,url):
        
        res = self.sess.get(url).text
        
        with open('jd.html', 'w', encoding='utf-8') as a:
            a.write(res)
                
        soup = BeautifulSoup(res, 'html.parser')
        
        li_lst = soup.find_all('li',attrs={'class':'gl-item'})
        
        item_lst = []
        
        #解析网页元素，bs4
        for i in li_lst:
            #sku#
            sku = i['data-sku']
            #########
            
            #img
            img = i.find('div',attrs={'class':'p-img'})
            if img:
                img = img.find('img')
                if img:
                    img = img.get('data-lazy-img')
            ##########
            
            #price
            price = i.find('div',attrs = {'class':'p-price'})
            if price:
                price = price.find('i')
                if price:
                    price = price.get_text()
            #########
            
            #text_
            text_ = i.find('div',attrs = {'class':'p-name p-name-type-2'})
            if text_:
                text_ = text_.find('em')
                if text_:
                    text_ = text_.get_text()
            ##########
            
            #comment p-commit
            comment = i.find('div',attrs = {'class':'p-commit'})
            if comment:
                comment = comment.find('a')
                if comment:
                    comment = comment.get_text()
            #########
            
            #coment_herf
            coment_herf = i.find('div',attrs = {'class':'p-commit'})
            if coment_herf:
                coment_herf = coment_herf.find('a')
                if coment_herf:
                    coment_herf = coment_herf['href']
            #########
            
            #shop_name
            shop_name = i.find('div',attrs={'class':'p-shop'})
            if shop_name:
                shop_name = shop_name.find('a')
                if shop_name:
                    shop_name = shop_name.get_text()
            #########
            
            #shop_href
            shop_href = i.find('div',attrs={'class':'p-shop'})
            if shop_href:
                shop_href = shop_href.find('a')
                if shop_href:
                    shop_href = shop_href['href']
            #########
            
            #area
            area = i.find('div',attrs = {'class':'p-stock hide'})
            if area:
                area = area.get('data-province')
            ##########
            
            
            item_lst.append([sku, img,price,text_,comment,coment_herf,shop_name,shop_href,area])
            print(item_lst)
        
        #收集的二位列表转pandas，df结构    
        df = pd.DataFrame(item_lst)
        
        # 写入csv文件
        df.to_csv(self.file_name, mode='a', index=False, header=False, encoding='utf-8-sig')
        
        
        
        return item_lst       
        
    
    def start_spider(self):
        
        for page in range(1,self.end_page+1):
            
            url = self.start_url+'&page='+str(page)
            
            print(url)
            
            print('关键词:'+self.keyword+'--第'+str(page)+'页')
            
            #请求间隔
            time.sleep(2)
            
            #带着url启动请求函数
            result = self.get_item_info(url)
            
            print(result)
            
        return '执行完毕'
            
            
            
        

            


if __name__ == "__main__":             
    #复制cookie     传入地区#area       #iploc                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    cookie_str = ''
        
    # 输入cookie，关键词，抓取页数
    #启动spider类
    content_page = Spider(cookie_str, 'iphone15', 2)
    #启动爬虫，根据页数循环请求
    response = content_page.start_spider()
    
    print(response)
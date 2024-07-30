# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import pandas as pd


class ShopeeRemarkPipeline:
    
    def __init__(self):
        self.file_name = 'shopee_remarks.csv'
        # Check if file already exists, if not create it and write the header
        if not os.path.exists(self.file_name):
            df = pd.DataFrame(columns=[
                'orderid', 'itemid', 'userid', 'shopid', 'rating_star',
                'author_username', 'product_items_name', 'product_items_image',
                'user_comment', 'Merchant_response', 'region'
            ])
            df.to_csv(self.file_name, index=False, encoding='utf-8-sig')    
            
            
    def process_item(self, item, spider):
        # Convert item to DataFrame
        df = pd.DataFrame([dict(item)])
        
        # Append the data to the CSV file
        df.to_csv(self.file_name, mode='a', index=False, header=False, encoding='utf-8-sig')
        print(item)
        return item

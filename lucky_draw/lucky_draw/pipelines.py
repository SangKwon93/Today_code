# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from matplotlib import collections
import pymongo


class LuckyDrawPipeline:
    def process_item(self, item, spider):
      pass
      
      
      
      # AWS상 mongoDB 구축할 경우 활용
        # client = pymongo.MongoClient('mongodb://team04:1111@ec2-54-95-8-243.ap-northeast-1.compute.amazonaws.com:27017/')
        # db = client.resell
        
      
        # data = {"pro_code": item["code"],
        #         "Model_fullname": item["name_en"],
        #          "Release_date": item["release_date"],
        #          "Release_Price": item["price"], 
        #          "img_url_1": item["img_url_1"],
        #          "img_url_2": item["img_url_2"],
        #          "img_url_3": item["img_url_3"],
        #          "img_url_4": item["img_url_4"]                   
        #        }
     
        # db.draw.insert_one(data)
    
        # return item

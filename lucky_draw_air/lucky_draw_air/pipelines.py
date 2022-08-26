# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from matplotlib import collections
import pymongo


class LuckyDrawAirPipeline:
    def process_item(self, item, spider):
    
        client = pymongo.MongoClient('mongodb://skpark:sk138029@localhost:27017/')
        db = client.project
        
        #"title": item["article_title"]
        data = {"pro_code": item["code"],
                "_id": item["_id"],
                 "Release_date": item["release_date"],
                 "Release_Price": item["price"], 
                 "img_url_1": item["img_url_1"],
                 "img_url_2": item["img_url_2"],
                 "img_url_3": item["img_url_3"],
                 "img_url_4": item["img_url_4"]                
               }
    
        # "img": item["img"],
        db.draw.insert_one(data)
        return item
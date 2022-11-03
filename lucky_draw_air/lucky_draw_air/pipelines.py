# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo



class LuckydrawPipeline:
  def process_item(self, item, spider):
      user = 'psk'
      pw = '1234'
      host = 'ec2-3-39-24-39.ap-northeast-2.compute.amazonaws.com'
      client = pymongo.MongoClient(f'mongodb://{user}:{pw}@{host}:27017/admin')
      db = client.resell
      
     
      data = {"pro_code": item["code"],
              "Model_fullname": item["_id"],
                "Release_date": item["release_date"],
                "Release_Price": item["price"], 
                "img_url_1": item["img_url_1"],
                "img_url_2": item["img_url_2"],
                "img_url_3": item["img_url_3"],
                "img_url_4": item["img_url_4"]                   
              }
    
      db.draw.insert_one(data)

      return item

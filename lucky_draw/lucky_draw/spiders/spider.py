import scrapy
import json
import requests
from scrapy.http import TextResponse
from bs4 import BeautifulSoup
import os
import threading
from multiprocessing import Process
import time
from fake_useragent import UserAgent
import urllib.request
import datetime as dt
from datetime import datetime


headers = {"User-Agent" : UserAgent().chrome }
#res = requests.get(url,headers=headers)

from lucky_draw.items import LuckyDrawItem


class Spider(scrapy.Spider):
    name="lucky_draw"
    allow_dimain=["https://www.luck-d.com/"]
    start_urls = ["https://www.luck-d.com/"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

   
        
    def parse(self, response):
        url_list=[]
        soup = BeautifulSoup(response.text)
        tm1 = soup.select('div.agent_site_info > h5 ')
        #url_list= response.xpath('//*[@id="ogIntro"]/div[2]/div/div/div/div[2]/h5/a/@href').extract()+response.xpath('//*[@id="ogIntro"]/div[4]/div/div/div/div[2]/h5/a/@href').extract()+response.xpath('//*[@id="ogIntro"]/div[6]/div/div/div/div[2]/h5/a/@href').extract()
        
        for tt in tm1:
            url_list.append(tt.select_one('a')['href'])
          
        for ttt in url_list:
            link = response.urljoin(ttt)
        
            yield scrapy.Request(link,callback=self.detail_info)
        
    def detail_info(self,response):
        item = LuckyDrawItem()
        # global title
        # title = response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()
        # release = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first()
        # price = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
        # lucky= dt.datetime.strptime(release,'%Y년 %m월 %d일') 
        # now = dt.datetime.today()
        
        soup = BeautifulSoup(response.text)
        global price
        price = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
        global title
        title = response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()
        
        # 가격이 있으면서 Jordan인 제품
        if price != '-' and "Jordan" in title :
            
            release = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first() 
        
            # ye_lucky= dt.datetime.strptime(release,'%Y년')
            # mo_lucky= dt.datetime.strptime(release,'%Y년 %m월')
            if '월' in release and '일' in release:
                global now
                now = dt.datetime.today()
                global lucky       
                lucky= dt.datetime.strptime(release,'%Y년 %m월 %d일')
                
                # 신제품 확인하기(현재보다 발매일이 이후인 경우)
                if now < lucky:
                    #lucky= dt.datetime.strptime(release,'%Y년 %m월 %d일') 
                    #now = dt.datetime.today()    
                    item = LuckyDrawItem()  
                    soup = BeautifulSoup(response.text)
                    item["code"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[2]/span/text()').extract_first()
                    item["name_en"]=response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()                     
                    item["release_date"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first()                           
                    item["price"] =response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
    
                    item['img_url_1']=response.xpath('//*[@id="product-carousel"]/div/div[1]/img/@src').extract_first()
                    item['img_url_2']=response.xpath('//*[@id="product-carousel"]/div/div[2]/img/@src').extract_first()
                    item['img_url_3']=response.xpath('//*[@id="product-carousel"]/div/div[3]/img/@src').extract_first()
                    item['img_url_4']=response.xpath('//*[@id="product-carousel"]/div/div[4]/img/@src').extract_first()
                  
                    yield item
                
      
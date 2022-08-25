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
from lucky_draw_air.logerr import logerr

headers = {"User-Agent" : UserAgent().chrome }
#res = requests.get(url,headers=headers)

from lucky_draw_air.items import LuckyDrawAirItem


class Spider(scrapy.Spider):
    name="lucky_draw_air"
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
        
        for tt in tm1:
            url_list.append(tt.select_one('a')['href'])
            
        for ttt in url_list:
            link = response.urljoin(ttt)
            yield scrapy.Request(link,callback=self.detail_info)
        
        # 오류 시 확인 할 수 있도록 기록을 남기려다가 실패 -> 추후 수정 필요
        # if url_list is not None:
        #     #logerr({"name": "k"})
        #     logerr({"date": "신규 제품 없습니다."})
        #     self.exitcode = 1
        #      # 강제종료코드

        # logerr({"date": "신규 제품 있습니다."})
        
        # 신규 등록 발매 정보만 가져오기
        # url_list= response.xpath('//*[@id="ogIntro"]/div[2]/div/div/div/div[2]/h5/a/@href').extract()
        # for link in url_list:
        #     link = response.urljoin(link)
        #     yield scrapy.Request(link,callback=self.detail_info)
        
    def detail_info(self,response):
        item = LuckyDrawAirItem()
        soup = BeautifulSoup(response.text)
        global price
        price = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
        global title
        title = response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()
        
        # 가격이 있으면서 제품명에 대문자 Jordan과 소문자 jordan인 경우
         
        if price != '-' and ("Jordan" in title or 'jordan' in title) :
        # if price != '-' :
            
            release = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first() 
        
      
            # 월과 일이 있는 경우 현재일자와 비교
            if '월' in release and '일' in release:
                global now
                now = dt.datetime.today()
                global lucky       
                lucky= dt.datetime.strptime(release,'%Y년 %m월 %d일')
                if now < lucky:
                    #lucky= dt.datetime.strptime(release,'%Y년 %m월 %d일') 
                    #now = dt.datetime.today()    
                    item = LuckyDrawAirItem()  
                    soup = BeautifulSoup(response.text)
                    item["code"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[2]/span/text()').extract_first()
                    item["_id"]=response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()                     
                    item["release_date"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first()                           
                    item["price"] =response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
                    item['img_url_1']=response.xpath('//*[@id="product-carousel"]/div/div[1]/img/@src').extract_first()
                    item['img_url_2']=response.xpath('//*[@id="product-carousel"]/div/div[2]/img/@src').extract_first()
                    item['img_url_3']=response.xpath('//*[@id="product-carousel"]/div/div[3]/img/@src').extract_first()
                    item['img_url_4']=response.xpath('//*[@id="product-carousel"]/div/div[4]/img/@src').extract_first()
                    
                    yield item
        #item["name_ko"]=response.xpath('//*[@id="ogIntro"]/h3/text()').extract_first()
        # item["prod_code"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[2]/span/text()').extract_first()
        # item["name_en"]=response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()
        # item["release_date"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first()
        # item["price"] =response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
        # item['img_url']=soup.select_one('#product-carousel > div > div:nth-child(3) > img')['src']
        # url_temp= item['img_url']
        # full_name= item["name_en"]+'.jpg'
        # item['img']= urllib.request.urlretrieve(url_temp, full_name)
    
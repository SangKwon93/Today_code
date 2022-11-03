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
from lucky_draw_air.items import LuckyDrawAirItem

headers = {"User-Agent" : UserAgent().chrome }

class Spider(scrapy.Spider):
    name="luckydraw"
    allow_dimain=["https://www.luck-d.com/"]
    start_urls = ["https://www.luck-d.com/"]
    # pip install scrapy-fake-useragent 패키지 미들웨어를 사용한다.
    # 미들웨어 == 연결하기 직전 과정 (header 검사도 미들웨어 하나의 과정)
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }
    # 상세 페이지 접속
    def parse(self, response):
        url_list= response.xpath('//*[@id="ogIntro"]/div[2]/div/div/div/div[2]/h5/a/@href').extract()
        for link in url_list:
            link = response.urljoin(link)
            yield scrapy.Request(link,callback=self.detail_info)

    # 상세 페이지 수집
    def detail_info(self,response):
        item = LuckyDrawAirItem()
        
        # 가격
        price = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
        
        # 제품명
        title = response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()
        
        # 일자
        release = response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first() 
        
        # 가격이 없고 조던이 있는 제품명만 추출
        if price != '-' and ("Jordan" in title or 'jordan' in title) :    
            
            # 월,일이 있는 경우만 수집(년도는 다 있음)
            if '월' in release and '일' in release:
                
                # 현재일자 
                now_date = dt.datetime.today()
                
                # 새 상품 발매일자
                item_date= dt.datetime.strptime(release,'%Y년 %m월 %d일')
                
                # 새 상품만 추출(데이터 확인해보니 재발매되는 제품들도 존재)
                if now_date < item_date:
                    item = LuckyDrawAirItem() 
                    item["code"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[2]/span/text()').extract_first()
                    item["_id"]=response.xpath('//*[@id="ogIntro"]/h5/text()').extract_first()                     
                    item["release_date"]=response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[3]/span/text()').extract_first()                           
                    item["price"] =response.xpath('//*[@id="ogIntro"]/div[3]/div[1]/label[4]/span/text()').extract_first()
                    item['img_url_1']=response.xpath('//*[@id="product-carousel"]/div/div[1]/img/@src').extract_first()
                    item['img_url_2']=response.xpath('//*[@id="product-carousel"]/div/div[2]/img/@src').extract_first()
                    item['img_url_3']=response.xpath('//*[@id="product-carousel"]/div/div[3]/img/@src').extract_first()
                    item['img_url_4']=response.xpath('//*[@id="product-carousel"]/div/div[4]/img/@src').extract_first()
                    
                    yield item
 
# -*- coding: utf-8 -*-
import scrapy
from time import sleep

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['ria.ru']
    start_urls = [
        'https://ria.ru/politics/',
        'https://ria.ru/society/',
        'https://ria.ru/science/',
        'https://ria.ru/culture/',
        'https://ria.ru/world/',
        'https://ria.ru/economy/',
        'https://ria.ru/religion/'
        ]

    def parse(self, response):
        urls = response.css('.list-item > a::attr(href)').extract()

        label = 'no'
        if 'politics' in response.url:
            label = 'politics'
        elif 'society' in response.url:
            label = 'society'
        elif 'science' in response.url:
            label = 'science'
        elif 'culture' in response.url:
            label = 'culture'
        elif 'world' in response.url:
            label = 'world'
        elif 'economy' in response.url:
            label = 'economy'
        elif 'religion' in response.url:
            label = 'religion'

        for url in urls:
            url = response.urljoin(url)
            self.log(f"Открываю {url}")

            yield scrapy.Request(url, callback=self.parse_detail_page, meta={'y':label})
        
        
        if response.css("div.list-items-loaded").extract():
            next_page_url = response.css("div.list-items-loaded::attr(data-next-url)").extract_first()
        else:
            next_page_url = response.css("div.list-more::attr(data-url)").extract_first()

        next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(next_page_url, callback=self.parse)
        


    def parse_detail_page(self, response):
        y = response.meta.get('y')
        sleep(1)
        yield{
            "title": response.css(".article__header > h1.article__title::text").extract_first(),
            "text": " ".join(response.css("div.article__body div.article__text::text").extract()), # Не экстрактит теги внутри дива типо <strong> и тд
            "label": y,
        }
        
            

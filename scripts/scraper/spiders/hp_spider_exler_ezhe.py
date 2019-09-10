#!/usr/bin/python
# -*- coding: utf-8 -*-

# scraper for snorapp, dr-piliulkin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpiderOld(CrawlSpider):
    name = "hp_exler_ezhe"
    allowed_domains = ["exler.ru"]
    start_urls = [
        "http://www.exler.ru/ezhe03/16-07-2015.htm"
    ]

    rules = (
        Rule(
            LinkExtractor(
                # allow=('http://borisakunin.livejournal.com/\d+\.html',),
                # deny=('tag', 'reply', 'thread', 'page'),
                # xpath for snorapp:
                restrict_xpaths=('//td[@id="NumberC"]/table/tr/td[1]')
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        list(self.parse_page(response))

    def parse_page(self, response):

        # use scrapy shell to find xpath
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        item = ScraperItem()
        item['url'] = response.url
        try:
            #item['title'] = response.xpath("//div[@class='BlogTopic']/a/text()").extract()[0]
            item['title'] = response.xpath("//table[@id='MainPage']/tr/td[1]/p[1]//text()").extract()[0]
        except IndexError:
            item['title'] = ""
        #item['text'] = " ".join(response.xpath("//div[@id='comm0']/child::node()").extract())
        #item['date'] = response.xpath("//td[@class='BlogSmall']/a/text()").extract()[0]
        #item['comment_count'] = str(len(response.xpath("//table[@id='MainPage']/tr/td/table[4]/tr").extract()) - 1)

        item['text'] = " ".join(response.xpath("//table[@id='MainPage']/tr/td[1]//text()").extract())
        try:
            item['date'] = " ".join(response.xpath("//table[@id='MainPage']/tr/td[1]//table//text()").extract()).split(u":\xa0")[1].split(" ")[0]
        except IndexError:
            item['date'] = response.url.split("/")[4].split(".htm")[0]
        try:
            item['comment_count'] = int(" ".join(response.xpath("//table[@id='MainPage']/tr/td[1]//table//text()").extract()).split("(")[1].split(")")[0])
        except IndexError:
            item['comment_count'] = 0
        yield item

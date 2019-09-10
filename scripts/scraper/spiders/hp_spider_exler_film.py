#!/usr/bin/python
# -*- coding: utf-8 -*-

# scraper for snorapp, dr-piliulkin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpiderOld(CrawlSpider):
    name = "hp_exler_film"
    allowed_domains = ["exler.ru"]
    start_urls = [
        #"http://www.exler.ru/blog/item/17500/"
        "http://www.exler.ru/films/20-02-2016.htm",
        #"http://www.exler.ru/likbez/13-01-2016.htm",
        #"http://www.exler.ru/expromt/17-02-2016.htm",
        #"http://www.exler.ru/bannizm/19-02-2016.htm"
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
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        item = ScraperItem()
        item['url'] = response.url
        try:
            #item['title'] = response.xpath("//div[@class='BlogTopic']/a/text()").extract()[0]
            item['title'] = response.xpath("//div[@id='article']/p/b/text()").extract()[0]
        except IndexError:
            item['title'] = ""
        #item['text'] = " ".join(response.xpath("//div[@id='comm0']/child::node()").extract())
        #item['date'] = response.xpath("//td[@class='BlogSmall']/a/text()").extract()[0]
        #item['comment_count'] = str(len(response.xpath("//table[@id='MainPage']/tr/td/table[4]/tr").extract()) - 1)

        item['text'] = " ".join(response.xpath("//div[@id='article']/p").extract())
        try:
            item['date'] = response.xpath("//div[@id='article']/table/tr[1]/td[1]/span[1]/table/tr[1]/td[2]/p/text()").extract()[0].split(":")[1]
        except IndexError:
            item['date'] = ""
        try:
            item['comment_count'] = int(response.xpath("//div[@id='article']/table/tr[1]/td[1]/span[1]/table/tr[1]/td[1]/a/text()").extract()[0].split("(")[1].split(")")[0])
        except IndexError:
            item['comment_count'] = ""
        yield item

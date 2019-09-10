#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la dglu
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_mantrabox"
    allowed_domains = ["mantrabox.livejournal.com"]
    start_urls = [
        # "http://mantrabox.livejournal.com/804564.html"
        "http://mantrabox.livejournal.com/805606.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('http://mantrabox.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page'),
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
            item['title'] = response.xpath(
                "//td[@class='caption']/text()").extract()[0]
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = response.xpath(
                "//table[@class='entrybox']/tr[1]/td[1]/table/tr[2]/td[1]").extract()[0]

        except IndexError:
            item['text'] = ''

        try:
            date = response.xpath("//td[@class='index']/text()").extract()[5]
            time = response.xpath("//td[@class='index']/b/text()").extract()[0]
            item['date'] = date, time
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = len(
                response.xpath("//div[@class='ljcmt_full']"))
        except IndexError:
            item["comment_count"] = "0"

        yield item

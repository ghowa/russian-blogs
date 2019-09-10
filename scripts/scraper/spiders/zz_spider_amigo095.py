#!/usr/bin/python
# -*- coding: utf-8 -*-

# 10 per page a la prilepin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request


class ZZSpider(CrawlSpider):
    name = "zz_amigo095"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://prilepin.livejournal.com/2007/03/"
        "http://amigo095.livejournal.com/2013/10/"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('amigo095.livejournal.com/\d\d\d\d/\d\d/',),
                deny=('amigo095.livejournal.com/\d\d\d\d/\d\d/\d\d',
                      'tag', 'reply', 'thread', 'page'),
            ),
            callback='parse_overview',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=('http://amigo095.livejournal.com/\d+/.html',),
                deny=('tag', 'reply', 'thread', 'page'),
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        list(self.parse_overview(response))

    def parse_overview(self, response):
        urls = response.xpath(
            "//td[@class='entry']/a/@href"
        ).extract()
        for url in urls:
            print url
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):

        # use scrapy shell to find xpath
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        item = ScraperItem()

        item["url"] = response.url

        item["date"] = " ".join(
            response.xpath(
                "//div[@class='entryDate'][1]/child::node()").extract())

        item["text"] = " ".join(
            response.xpath("//td[@class='entry'][2]/child::node()").extract())

        try:
            item["title"] = response.xpath(
                "//div[@class='entryHeader']/text()").extract()[0]
        except IndexError:
            item["title"] = ""

        try:
            item["comment_count"] = response.xpath(
                "//div[@class='entryComments']/a[1]/text()").extract()[0]

        except IndexError:
            item["comment_count"] = "0"

        yield item

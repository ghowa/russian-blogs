#!/usr/bin/python
# -*- coding: utf-8 -*-

# 10 per page a la prilepin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request


class ZZSpider(CrawlSpider):
    name = "zz_ru-bykov"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://ru-bykov.livejournal.com/2014/10/"
        "http://ru-bykov.livejournal.com/2015/07/"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('ru-bykov.livejournal.com/\d\d\d\d/\d\d/',),
                deny=('ru-bykov.livejournal.com/\d\d\d\d/\d\d/\d\d',
                      'tag', 'reply', 'thread', 'page'),
            ),
            callback='parse_overview',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=('http://ru-bykov.livejournal.com/\d+/.html',),
                deny=('tag', 'reply', 'thread', 'page'),
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        list(self.parse_overview(response))

    def parse_overview(self, response):
        urls = response.xpath("//div[@class='daysubjects']/a/@href").extract()
        for url in urls:
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):

        # use scrapy shell to find xpath
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        item = ScraperItem()

        item["url"] = response.url

        item["user"] = response.xpath(
            "//a[@class='i-ljuser-username'][2]/b/text()").extract()[0]

        item["date"] = response.xpath(
            "//span[@class='entryHeaderDate']/text()").extract()[0]

        item["text"] = " ".join(
            response.xpath("//div[@class='entryText']/child::node()").extract())

        try:
            item["title"] = response.xpath(
                "//div[@class='body-title']/text()").extract()[0]
        except IndexError:
            item["title"] = ""

        try:
            item["comment_count"] = response.xpath(
                "//div[@class='entryLinkbar']/ul/li[1]/a/text()").extract()[0]
        except IndexError:
            item["comment_count"] = "0"

        yield item

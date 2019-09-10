#!/usr/bin/python
# -*- coding: utf-8 -*-

# 10 per page a la prilepin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request


class ZZSpider(CrawlSpider):
    name = "zz_prilepin"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://prilepin.livejournal.com/2007/03/"
        #"http://prilepin.livejournal.com/2014/10/"
        "http://prilepin.livejournal.com/2015/07/"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('prilepin.livejournal.com/\d\d\d\d/\d\d/',),
                deny=('prilepin.livejournal.com/\d\d\d\d/\d\d/\d\d',
                      'tag', 'reply', 'thread', 'page'),
            ),
            callback='parse_overview',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=('http://prilepin.livejournal.com/\d+/.html',),
                deny=('tag', 'reply', 'thread', 'page'),
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        list(self.parse_overview(response))

    def parse_overview(self, response):
        urls = response.xpath("//dd/a/@href").extract()
        for url in urls:
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):

        # use scrapy shell to find xpath
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        item = ScraperItem()

        item["url"] = response.url

        item["date"] = response.xpath(
            "//p[@class='entry-footer']/text()").extract()[0]

        item["text"] = " ".join(
            response.xpath(
                "//div[@class='entry-body']/child::node()").extract())

        try:
            item["title"] = response.xpath(
                "//h3[@class='entry-header']/text()").extract()[0]
        except IndexError:
            item["title"] = ""

        try:
            item["comment_count"] = response.xpath(
                "//p[@class='entry-footer']/a[3]/text()").extract()[0]
        except IndexError:
            item["comment_count"] = "0"

        yield item

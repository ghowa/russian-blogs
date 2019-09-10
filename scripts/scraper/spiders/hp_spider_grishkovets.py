#!/usr/bin/python
# -*- coding: utf-8 -*-

# 10 per page a la prilepin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request


class ZZSpider(CrawlSpider):
    name = "hp_grishkovets"
    allowed_domains = ["odnovremenno.com"]
    start_urls = [
        # "http://prilepin.livejournal.com/2007/03/"
        # "http://prilepin.livejournal.com/2014/10/"
        # "http://odnovremenno.com/archives/category/diary"
        "http://odnovremenno.com/archives/date/2015",
        "http://odnovremenno.com/archives/date/2014",
        "http://odnovremenno.com/archives/date/2013",
        "http://odnovremenno.com/archives/date/2012",
        "http://odnovremenno.com/archives/date/2011",
        "http://odnovremenno.com/archives/date/2010",
        "http://odnovremenno.com/archives/date/2009",
        "http://odnovremenno.com/archives/date/2008"
    ]

    rules = (
        Rule(
            LinkExtractor(
                # allow=('http://odnovremenno.com/archives/\d\d\d\d',),
                # deny=(),
                restrict_xpaths=("//div[@class='nav']"),
            ),
            callback='parse_overview',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=('http://odnovremenno.com/archives/category/diary/page/\d+',),
                # deny=('tag', 'reply', 'thread', 'page'),
                # restrict_xpaths=("//div[@class='p-head']/h3/a/@href"),
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_start_url(self, response):
        list(self.parse_overview(response))

    def parse_overview(self, response):
        urls = response.xpath("//div[@class='p-head']/h3/a/@href").extract()
        for url in urls:
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):

        # use scrapy shell to find xpath
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        item = ScraperItem()

        item["url"] = response.url

        item["date"] = " ".join(response.xpath(
            "//small[@class='p-time']/child::node()/text()"
        ).extract())

        item["text"] = " ".join(response.xpath(
            "//div[@class='p-con']/child::node()"
        ).extract())

        try:
            item["title"] = response.xpath(
                "//div[@class='p-head']/h1/text()"
            ).extract()[0]
        except IndexError:
            item["title"] = ""
        try:
            item["comment_count"] = response.xpath("//div[@id='comments']/h2/text()").extract()[0]
        except IndexError:
            item["comment_count"] = 0

        yield item


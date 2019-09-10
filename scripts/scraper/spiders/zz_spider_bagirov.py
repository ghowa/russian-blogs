#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la dglu
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_bagirov"
    allowed_domains = ["bagirov.livejournal.com"]
    start_urls = [
        "http://bagirov.livejournal.com/446032.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('http://bagirov.livejournal.com/\d+\.html',),
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
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        item = ScraperItem()
        item['url'] = response.url

        try:
            item['title'] = response.xpath(
                "//div[@class='asset-header-content-inner']/h2/a/text()"
            ).extract()[0]
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = " ".join(response.xpath(
                "//div[@class='asset-content']/child::node()"
            ).extract())
        except IndexError:
            item['text'] = ''

        try:
            item['date'] = response.xpath("//abbr[@class='datetime']/text()").extract()[0]
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = response.xpath("//div[@class='comments-nav']/text()").extract()[0]
        except IndexError:
            item["comment_count"] = "0"

        yield item

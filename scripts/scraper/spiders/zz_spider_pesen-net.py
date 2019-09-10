#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la dglu
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_pesen-net"
    allowed_domains = ["pesen-net.livejournal.com"]
    start_urls = [
        "http://pesen-net.livejournal.com/82406.html"
        # adult: http://pesen-net.livejournal.com/71163.html
        #"http://pesen-net.livejournal.com/70709.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                deny=('tag', 'reply', 'thread', 'page'),
                restrict_xpaths=("//span[@class='entry-linkbar-inner']"),
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
        # inspect_response(response)

        item = ScraperItem()
        item['url'] = response.url

        try:
            item['title'] = response.xpath(
                "//dt[@class='entry-title']/text()").extract()[0]
        except IndexError:
            item['title'] = ""

        item['text'] = " ".join(
            response.xpath(
                "//div[@class='entry-content']/child::node()").extract())

        try:
            item['date'] = response.xpath(
                "//abbr[@class='updated']/text()").extract()[0]
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = response.xpath(
                "//span[@class='comments-count']/text()").extract()[0]
        except IndexError:
            item["comment_count"] = "0"

        yield item

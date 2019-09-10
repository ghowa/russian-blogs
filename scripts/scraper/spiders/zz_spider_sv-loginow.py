#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la dglu
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_sv-loginow"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://alex-aka-jj.livejournal.com/230838.html"
        #"http://alex-aka-jj.livejournal.com/3866.html"
        #"http://sv-loginow.livejournal.com/123512.html"
        "http://sv-loginow.livejournal.com/24451.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                deny=('tag', 'reply', 'thread', 'page'),
                restrict_xpaths=("//p[@class='prevnext']"),
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

        item['text'] = " ".join(response.xpath(
            "//div[@class='asset-body']/child::node()").extract())

        try:
            item['date'] = response.xpath(
                "//abbr[@class='datetime']/text()").extract()[0]
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = response.xpath(
                "//ul[@class='asset-meta-list']/li[1]/a/text()").extract()[0]
        except IndexError:
            item["comment_count"] = "0"

        yield item

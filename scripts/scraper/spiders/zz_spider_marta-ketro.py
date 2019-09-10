#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la dglu
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_marta-ketro"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://marta-ketro.livejournal.com/578294.html"
        "http://marta-ketro.livejournal.com/599491.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                # allow=('http://marta-ketro.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page'),
                restrict_xpaths=("//div[@class='b-singlepost-standout']"),
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
                "//div[@class='b-singlepost-wrapper']/h1/text()").extract()[0]
        except IndexError:
            item['title'] = ""

        item['text'] = " ".join(response.xpath(
            "//article[2]/child::node()").extract())

        try:
            date = response.xpath("//time/a/text()").extract()
            date.append(response.xpath("//time/text()[3]").extract()[0])
            item['date'] = " ".join(date)
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = response.xpath(
                "//span[@class='js-amount'][1]/text()").extract()
        except IndexError:
            item["comment_count"] = "0"

        yield item

#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la tanyant
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_izubr"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://tanyant.livejournal.com/118267.html"
        #"http://izubr.livejournal.com/230791.html"

    ]

    rules = (
        Rule(
            LinkExtractor(
                #allow=('http://tanyant.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page'),
                # xpath for snorapp, tanyant
                # restrict_xpaths=('//a[@title="Previous"]')
                restrict_xpaths=("//i[@class='b-controls-bg']/parent::a"),
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_page(self, response):

        # use scrapy shell to find xpath
        #from scrapy.shell import inspect_response
        #inspect_response(response)

        item = ScraperItem()
        item['url'] = response.url

        try:
            item['title'] = response.xpath(
                '//h3[@class="entry-header"]/text()'
            ).extract()[0]
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = " ".join(
                response.xpath('//div[@class="entry-body"]/child::node()').extract())
        except IndexError:
            item['text'] = ''

        try:
            item['date'] = response.xpath("//p[@class='entry-footer']/text()").extract()[0]
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = response.xpath(
                "//p[@class='entry-footer']/a/text()").extract()[2]
        except IndexError:
            item['comment_count'] = '0'

        yield item

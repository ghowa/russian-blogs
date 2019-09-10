#!/usr/bin/python
# -*- coding: utf-8 -*-

# scraper for snorapp, dr-piliulkin
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpiderOld(CrawlSpider):
    name = "zz_snorapp"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        "http://snorapp.livejournal.com/1445133.html"
        #"http://snorapp.livejournal.com/258210.html"
        #"http://snorapp.livejournal.com/1226321.html"
        #"http://snorapp.livejournal.com/1402399.html"
        #"http://snorapp.livejournal.com/1403583.html",
        #"http://snorapp.livejournal.com/258210.html",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('http://snorapp.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page'),
                # xpath for snorapp:
                restrict_xpaths=('//img[@title="Previous Entry"]/parent::a')
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
                '//dt[@class="entry-title"]/text()'
            ).extract()[0]
        except IndexError:
            item['title'] = ""
        item['text'] = " ".join(
            response.xpath('//div[@class="entry-content"]').extract())
        item['date'] = response.xpath(
            '//abbr[@class="updated"]/@title'
        ).extract()[0]
        try:
            item['comment_count'] = response.xpath(
                '//span[@class="comments-count"]/text()'
            ).extract()[0]
        except IndexError:
            item['comment_count'] = "0"

        yield item

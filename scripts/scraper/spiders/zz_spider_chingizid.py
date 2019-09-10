#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la tanyant
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_chingizid"
    allowed_domains = ["chingizid.livejournal.com"]
    start_urls = [
        "http://chingizid.livejournal.com/1461466.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('http://chingizid.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page'),
                # xpath for snorapp, tanyant
                # restrict_xpaths=('//a[@title="Previous"]')
                restrict_xpaths=("//div/h2/a[1]"),
            ),
            callback='parse_page',
            follow=True
        ),
    )

    def parse_page(self, response):

        # use scrapy shell to find xpath
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        item = ScraperItem()
        item['url'] = response.url

        try:
            item['title'] = response.xpath(
                '//h3/text()'
            ).extract()[0]
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = " ".join(
                response.xpath("//div[@class='body'][1]/child::node()").extract())

        except IndexError:

            item['text'] = ''

        try:
            item['date'] = response.xpath('//div[@class="index"][1]/a[1]/text()').extract()
        except IndexError:
            item['date'] = ''

        item['comment_count'] = response.xpath(
            '//div[@class="index"][1]/a[2]/text()'
        ).extract()

        yield item

#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la tanyant
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_maroosya"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://tanyant.livejournal.com/118267.html"
        #"http://maroosya.livejournal.com/69104.html"
        #"http://maroosya.livejournal.com/67463.html"
        #"http://maroosya.livejournal.com/28593.html"
        #"http://maroosya.livejournal.com/22238.html"
        #"http://maroosya.livejournal.com/15503.html"
        #"http://maroosya.livejournal.com/8153.html"
        #"http://maroosya.livejournal.com/4943.html"
        "http://maroosya.livejournal.com/3055.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                #allow=('http://tanyant.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page', 'update'),
                # xpath for snorapp, tanyant
                # restrict_xpaths=('//a[@title="Previous"]')
                restrict_xpaths=("//div[@class='j-l-alpha-content-inner']/div[1]"),
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
                "//h3[@class='j-e-title']/child::node()/text()"
            ).extract()[0]
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = " ".join(
                response.xpath("//div[@class='j-e-text']/child::node()").extract()
            )
        except IndexError:

            item['text'] = ''

        try:
            time = response.xpath("//span[@class='j-e-date-time']/text()").extract()[0]
            date = response.xpath("//span[@class='j-e-date-day']/text()").extract()
            date.append(time)
            item['date'] = date
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = response.xpath("//div[@class='j-l-comments-inner']/ul[1]/li[1]/text()").extract()[0]
        except IndexError:
            item['comment_count'] = '0'

        yield item

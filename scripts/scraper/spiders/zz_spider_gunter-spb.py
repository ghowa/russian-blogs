#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la tanyant
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_gunter-spb"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        #"http://tanyant.livejournal.com/118267.html"
        #"http://gunter-spb.livejournal.com/14196.html"
        #"http://gunter-spb.livejournal.com/2387127.html"
        #"http://gunter-spb.livejournal.com/610032.html"
        "http://gunter-spb.livejournal.com/599654.html"
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
                '//h1/text()'
            ).extract()[0]
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = " ".join(
                response.xpath('//article[2]/child::node()').extract())

        except IndexError:

            item['text'] = ''

        try:
            time = response.xpath("//time[1]/text()[3]").extract()[0]
            date = response.xpath("//time[1]/a/text()").extract()
            date.append(time)
            item['date'] = date
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = response.xpath(
                '//span[@class="js-amount"]/text()'
            ).extract()[0]
        except IndexError:
            item['comment_count'] = '0'

        yield item

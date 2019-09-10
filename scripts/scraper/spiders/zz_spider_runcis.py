#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la tanyant
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_runcis"
    allowed_domains = ["livejournal.com"]
    start_urls = [
        "http://users.livejournal.com/_runcis/515083.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                #allow=('http://tanyant.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page'),
                # xpath for snorapp, tanyant
                # restrict_xpaths=('//a[@title="Previous"]')
                restrict_xpaths=("//img[@title='Previous Entry']/parent::a"),
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
                '//table[@class="entrybox"][1]/tr[1]/td[1]/table[1]/tr[1]/td[1]/text()'
            ).extract()[0]
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = " ".join(
                 response.xpath(
                    '//table[@class="entrybox"][1]/tr[1]/td[1]/table[1]/tr[2]/td[1]/child::node()'
                 ).extract())
        except IndexError:

            item['text'] = ''

        try:
            time = response.xpath( '//table[@class="entrybox"][1]/tr[1]/td[1]/table[1]/tr[1]/td[2]/text()').extract()[0]
            date = response.xpath( '//table[@class="entrybox"][1]/tr[1]/td[1]/table[1]/tr[1]/td[2]/text()').extract()

            date.append(time)
            item['date'] = date
        except IndexError:
            item['date'] = ''

        try:
            item['comment_count'] = len(response.xpath(
                '//table[@class="entrybox"][2]/tr[1]/td[1]/table[1]/tr[2]/td[1]/div'
            ).extract())
        except IndexError:
            item['comment_count'] = '0'

        yield item

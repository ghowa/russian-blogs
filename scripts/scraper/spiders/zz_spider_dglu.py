#!/usr/bin/python
# -*- coding: utf-8 -*-

# old ZZ a la dglu
from scrapy.contrib.spiders import CrawlSpider, Rule
from scraper.items import ScraperItem
from scrapy.contrib.linkextractors import LinkExtractor


class ZZSpider(CrawlSpider):
    name = "zz_dglu"
    allowed_domains = ["dglu.livejournal.com"]
    start_urls = [
        # "http://dglu.livejournal.com/174366.html"
        "http://dglu.livejournal.com/175360.html"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('http://dglu.livejournal.com/\d+\.html',),
                deny=('tag', 'reply', 'thread', 'page'),
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
                '//span[@class="subject"]/text()'
            ).extract()
        except IndexError:
            item['title'] = ""

        try:
            item['text'] = " ".join(
                response.xpath("//td[@class='entry']").extract())

        except IndexError:

            item['text'] = ''

        try:
            date = response.xpath('//th[@class="headerbar"][1]/text()').extract()
            time = response.xpath('//td[@class="metabar"]/em/text()').extract()[0]
            date.append(time)
            item['date'] = date
        except IndexError:
            item['date'] = ''

        item['comment_count'] = response.xpath(
            '//p[@class="comments"]/a[1]/text()'
        ).extract()

        yield item

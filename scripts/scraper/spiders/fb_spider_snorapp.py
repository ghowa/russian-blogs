from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import ScraperItem
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from scrapy.contrib.linkextractors import LinkExtractor
import sys
import os
import urlparse
import urllib
from scrapy import Request, Selector


class MFBSpider(CrawlSpider):

    name = "m_fb_sno"
    # allowed_domains = ["facebook.com"]

    urls = [
        'snorapp17-16.html',
        'snorapp16.html',
    ]

    def start_requests(self):
        reload(sys)
        print "STARTING 2........."
        sys.setdefaultencoding('utf8')
        urls = [
            'snorapp17-16.html',
            'snorapp16.html',
        ]
        for file in urls:
            # file = urlparse.urljoin('file:', urllib.pathname2url(os.path.abspath(file)))
            yield Request(file, self.parse_list)

    def parse_list(self, response):
        print response.url
        # use scrapy shell to find xpath
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for url in response.xpath("//a[@class='_5pcq']/@href").extract():
            url = "https://mobile.facebook" + url.split("facebook")[1]
            yield Request(url, self.parse_page)

    def parse_page(self, response):
        # use scrapy shell to find xpath
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        for element in response.xpath("//div[@id='m_story_permalink_view']/div[2]/div/div/div"):
            item = ScraperItem()
            item["url"] = response.url
            item["text"] = "".join(element.xpath("div[1]//text()").extract())
            try:
                item["date"] = element.xpath("div/abbr/text()").extract()[0]
                item["name"] = element.xpath("h3/a/text()").extract()[0]
            except IndexError:
                print "index error", response.url
            if len(item["text"]) > 0:
                yield item

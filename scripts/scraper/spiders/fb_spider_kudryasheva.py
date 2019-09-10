from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scraper.items import ScraperItem
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from scrapy.contrib.linkextractors import LinkExtractor


class FBSpider(CrawlSpider):

    name = "fb_kudryasheva"
    allowed_domains = ["facebook.com"]

    start_urls = [
        '/alya.khaitlina.html',
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=("facebook.com/alya.khaitlina/posts", "facebook.com/photo"),
                #allow=("facebook.com/TatyanaTolstaya", "facebook.com/photo"),
                restrict_xpaths='//a[@class="_5pcq"]'
            ),
            callback='parse_page', follow=True
        ),
    )

    def __init__(self, category=None, *args, **kwargs):
        super(FBSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Firefox()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def parse_page(self, response):

        # scrape dynamically generated HTML
        self.driver.get(response.url)
        hxs = Selector(text=self.driver.page_source)
        item = ScraperItem()

        # use scrapy shell to find xpath
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        try:
            divs = hxs.xpath(
                '//div[@id="contentArea"]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/descendant-or-self::*/text()'
            ).extract()
            text = u" ".join(divs[1:])
            no_text = len(divs) == 0
        except IndexError:
            no_text = True

        if no_text:
            try:
                text = " ".join(hxs.xpath(
                    '//span[@class="hasCaption"]/child::node()'
                ).extract())
            except IndexError:
                text = ""

        item['url'] = response.url
        item['text'] = text
        item['title'] = hxs.xpath('//title/text()').extract()
        item['date'] = hxs.xpath('//span[@class="timestampContent"]/text()').extract()

        comments = float(hxs.xpath('count(//abbr)').extract()[0]) - 1

        try:
            likes = hxs.xpath(
                '//div[@class="UFILikeSentenceText"]/span/span/text()'
            ).extract()[0]

            if "likes" in likes:
                like_count = 1.0
            else:
                try:
                    like_count = len(likes.split(", "))
                    if "others" in likes:
                        like_count += float(
                            likes.split("and ")[1].split(" others")[0]
                            .replace(",", "")
                        )
                    elif "and" in likes:
                        like_count += 1.0
                except IndexError:
                    like_count = 2.0
        except IndexError:
            like_count = 0.0
        # print "like count: "+str(like_count)

        try:
            shares = hxs.xpath(
                '//a[@class="UFIShareLink"]/text()'
            ).extract()[0]

            share_count = float(shares.split(" share")[0].replace(",", ""))
        except IndexError:
            share_count = 0.0

        print like_count, share_count, comments

        item['comment_count'] = [like_count, share_count, comments]

        yield item

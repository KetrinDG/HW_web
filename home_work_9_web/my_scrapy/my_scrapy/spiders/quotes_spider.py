import scrapy
import os


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": os.path.join("data", "qoutes.json"),
        "LOG_LEVEL": "ERROR",
    }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get(),
            }
        page = response.xpath("//li[@class='next']/a/@href").get()
        if page:
            yield scrapy.Request(url=self.start_urls[0] + page)

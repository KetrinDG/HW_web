import scrapy
import os


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    author_urls = []
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": os.path.join("data", "authors.json"),
        "LOG_LEVEL": "ERROR",
    }

    def parse(self, response):
        for author in response.xpath("/html//div[@class='quote']/span"):
            url = author.xpath("a/@href").get()
            if url and url not in self.author_urls:
                self.author_urls.append(url)
                yield scrapy.Request(
                    url=self.start_urls[0] + url, callback=self.get_author
                )

        page = response.xpath("//li[@class='next']/a/@href").get()
        if page:
            yield scrapy.Request(url=self.start_urls[0] + page)

    def get_author(self, response):
        author = response.xpath("/html//div[@class='author-details']")
        return {
            "fullname": author.xpath("h3/text()")
            .get()
            .replace("\n", "")
            .replace("-", " ")
            .strip(),
            "born_date": author.xpath("//span[@class='author-born-date']/text()").get(),
            "born_location": author.xpath(
                "//span[@class='author-born-location']/text()"
            ).get(),
            "description": author.xpath(
                "div[@class='author-description']/text()"
            ).get(),
        }

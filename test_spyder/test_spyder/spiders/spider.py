from typing import Any
import scrapy
from scrapy.http import Response


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings={"FEED_FORMAT":"json","FEED_URI":"quotes.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    custom_settings={"FEED_FORMAT":"json","FEED_URI":"authors.json"}
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self,response:Response):
        for i in response.xpath("/html//div[@class='quote']/span/a/@href").getall():
            yield scrapy.Request(callback=self.parse_authors,url=self.start_urls[0]+i)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


    def parse_authors(self, response: Response) -> Any:
        for author in response.xpath("/html//div[@class='author-details']"):
            yield {
                "fullname": author.xpath("h3[@class='author-title']/text()").get(),
                "born_date": author.xpath("p/span[@class='author-born-date']/text()").get(),
                "born_location": author.xpath("p/span[@class='author-born-location']/text()").get(),
                "description":author.xpath("div[@class='author-description']/text()").get().strip()
            }
        
            
import scrapy

from scrapy.loader import ItemLoader

from ..items import BannerbankItem
from itemloaders.processors import TakeFirst


class BannerbankSpider(scrapy.Spider):
	name = 'bannerbank'
	start_urls = ['https://www.bannerbank.com/about-us/news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="title field-title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="component list-pagination col-xs-12"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="title field-title"]/text()').get()
		description = response.xpath('//div[@class="content field-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="title-caption-section"]/text()').get()

		item = ItemLoader(item=BannerbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

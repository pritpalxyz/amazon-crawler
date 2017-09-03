# -*- coding: utf-8 -*-
import scrapy
from ecommspi.items import EcommspiCatagItem


class ProdextractSpider(scrapy.Spider):
	name = "prodextract"
	start_urls = ['http://www.amazon.in/Computer-Accessories/b/ref=sd_allcat_computers_accessories?ie=UTF8&node=1375248031']

	def parse(self, response):
		for href in response.xpath("//div[@class='categoryRefinementsSection']//li[@style='margin-left: 6px']//a/@href"):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parseProducts)


	def parseProducts(self,response):
		extract_catag = str(response.url)
		extract_catag = extract_catag.split('/')[3]
		for produrl in response.xpath("//img[@alt='Product Details']/../@href").extract():
			print produrl
			item = EcommspiCatagItem()
			item['prod_url'] = produrl
			item['prod_catag'] = extract_catag
			item['prod_catag_url'] = response.url
			yield item

		next_page = response.xpath("//span[@id='pagnNextString']/../@href")
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parseProducts)





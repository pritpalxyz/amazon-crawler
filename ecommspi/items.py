# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EcommspiCatagItem(scrapy.Item):
	prod_url 			= scrapy.Field()
	prod_catag 			= scrapy.Field()
	prod_catag_url 		= scrapy.Field()


class EcommSpiProductItem(scrapy.Item):
	prod_id			= scrapy.Field()  #mandatory
	title				= scrapy.Field() 	#mandatory
	site 				= scrapy.Field() 
	link 				= scrapy.Field() #mandatory
	description 		= scrapy.Field()
	brand 				= scrapy.Field()
	image_link 			= scrapy.Field()  #mandatory
	small_image_link 	= scrapy.Field()
	images 				= scrapy.Field()
	small_images 		= scrapy.Field()
	gender 				= scrapy.Field()
	product_category 	= scrapy.Field()  #mandatory
	sub_category 		= scrapy.Field()
	price 				= scrapy.Field() #mandatory
	available 			= scrapy.Field()  #mandatory
	breadcrumb	 		= scrapy.Field()  #mandatory
	metadata 			= scrapy.Field()
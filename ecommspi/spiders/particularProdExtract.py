# -*- coding: utf-8 -*-
import scrapy ,re , json
from ecommspi.items import EcommSpiProductItem
from bs4 import BeautifulSoup
from ecommspi.mydb import amazonDB

class ProdextractSpider(scrapy.Spider):
	name = "parseParticulatProd"
	start_urls = ['http://www.amazon.in/Sandisk-Cruzer-force-durable-casing/dp/B00C9Q5PGM']

	def __init__(self):
		db = amazonDB()
		self.db = db.dbb



	def parse(self,response):
		cursor = self.db.cursor()
		sql = """ SELECT prod_url FROM amazon_prod WHERE update_stat = '0' """
		cursor.execute(sql)
		all_prod = cursor.fetchall()
		for i in all_prod:
			yield scrapy.Request(i[0], callback=self.parse_product)




	def parse_product(self, response):
		item = EcommSpiProductItem()
		idd = str(response.url)
		idd = idd.split('/')[-1]
		title = response.xpath("//span[@id='productTitle']/text()").extract()
		title = self.list_to_str(title)
		title = self.cleanText(self.parseText(title))

		description = response.xpath("//div[@id='productDescription']/p//text()").extract()

		description = self.list_to_str(description)
		description = self.cleanText(self.parseText(description))


		brand = response.xpath("//td[text()='Brand']/following-sibling::td/text()").extract()
		brand = self.list_to_str(brand)
		brand = self.cleanText(self.parseText(brand))

		try:
			product_category = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']//span/a/text()").extract()[2]
			product_category = self.cleanText(self.parseText(product_category))

		except:
			product_category = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']//span/a/text()").extract()[0]
			product_category = self.cleanText(self.parseText(product_category))

		try:
			sub_category = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']//span/a/text()").extract()[3]
			sub_category = self.cleanText(self.parseText(sub_category))
		except:
			sub_category = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']//span/a/text()").extract()[1]
			sub_category = self.cleanText(self.parseText(sub_category))


		price = response.xpath("//tr[@id='priceblock_ourprice_row']/td[2]/span[@class='a-size-medium a-color-price']/text()").extract()
		price = self.list_to_str(price)
		price = self.cleanText(self.parseText(price))

		if price == '':
			price = response.xpath("//span[@id='priceblock_saleprice']/text()").extract()
			price = self.list_to_str(price)
			price = self.cleanText(self.parseText(price))

		stock = response.xpath("//div[@id='outOfStock']")

		if stock:stock = False
		else:stock = True

		breadcrumb = response.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']//a/text()").extract()
		breadcrumb = self.makebreabcrumb(breadcrumb)
		breadcrumb = self.cleanText(self.parseText(breadcrumb))

		allsmallimages = response.xpath(".//*[@id='imageBlock']/div/div//span[@class='a-button-text']//img/@src").extract()
		allsmallimages = json.dumps(allsmallimages)


		gethtml = response.xpath("//div[@class='column col1 ']//div[@class='attrG']//table//tr").extract()
		metadatalist = self.createListToData(gethtml)
		metadatalist = json.dumps(metadatalist)

		item['prod_id'] = idd
		item['title'] = title
		item['site'] = 'amazon'
		item['link'] = response.url
		item['description'] = description
		item['brand'] = brand
		item['image_link'] = response.xpath("//img[@id='landingImage']/@src").extract()[0]
		item['small_image_link'] = allsmallimages
		item['gender'] = ''
		item['product_category'] = product_category
		item['sub_category'] =  sub_category
		item['price'] = price
		item['available'] = stock
		item['breadcrumb'] = breadcrumb
		item['metadata'] = metadatalist
		yield item

	def createListToData(self,lists):
		mylist = []
		for i in lists:
			soup = BeautifulSoup(i)
			title = soup.findAll('td')[0].text
			value = soup.findAll('td')[1].text
			if title == '\u00a0':continue
			try:
				title = str(title)
				title = title.replace("'","")
			except:pass
			try:
				value = str(value)
				value = value.replace("'","")
			except:pass

			mydict = {'title':title,'value':value}
			mylist.append(mydict)
		return mylist

	def makebreabcrumb(self,lll):
		dumm = ""
		for i in lll:dumm = "%s>%s"%(dumm,i)
		return dumm


	def list_to_str(self,mylist):
		dumm = ""
		for i in mylist:dumm = "%s %s"%(dumm,i)
		return dumm


	def parseText(self, str):
		soup = BeautifulSoup(str, 'html.parser')
		return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()

	def cleanText(self,text):
		soup = BeautifulSoup(text,'html.parser')
		text = soup.get_text();
		text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
		text = text.replace("'","")
		return text 

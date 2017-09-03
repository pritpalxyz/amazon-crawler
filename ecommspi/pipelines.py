# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ecommspi.mydb import amazonDB
import MySQLdb
import psycopg2


class EcommspiPipeline(object):

	def __init__(self):
		db = amazonDB()
		self.db = db.dbb



	def process_item(self, item, spider):
		self.spidername =  str(spider.name)
		cursor = self.db.cursor()

		if self.spidername == 'prodextract':
			checksql = """ SELECT * FROM amazon_prod WHERE prod_url = '%s'  LIMIT 1 """%(item['prod_url'])
			try:
				cursor.execute(checksql)
				old_prod = cursor.fetchone()
			except :pass

			if old_prod is None:
				sql = """  INSERT INTO amazon_prod (prod_url,prod_catag,prod_catag_url)  VALUES ('%s','%s','%s') """%(item['prod_url'],item['prod_catag'],item['prod_catag_url'])
				try:
					cursor.execute(sql)
					self.db.commit()
					print sql
				except psycopg2.OperationalError as e:
					print "ERROR:::::%s"%(e)
					print "some Error"
					self.db.rollback()
			
		elif self.spidername == 'parseParticulatProd':
			updatesql = """ UPDATE amazon_prod SET prod_id = '%s',
							title ='%s',
							site  = '%s' ,
							link  = '%s' ,
							description = '%s' ,
							brand  = '%s',
							image_link  = '%s' ,
							small_image_link  = '%s',
							images   = '%s',
							small_images   ='%s'  ,
							gender  = '%s',
							product_category  = '%s',
							sub_category  = '%s' ,
							price   = '%s',
							available ='%s' ,
							breadcrumb  = '%s',
							metadata   = '%s',
							update_stat  = '1' WHERE prod_url = '%s' """%(item['prod_id'],item['title'],item['site'],item['link'],item['description'],item['brand'],item['image_link'],item['small_image_link'],'','',item['gender'],item['product_category'],item['sub_category'],item['price'],item['available'],item['breadcrumb'],item['metadata'],item['link'])
			try:
				cursor.execute(updatesql)
				self.db.commit()
				cursor.close()
				print updatesql
			except psycopg2.OperationalError as e:
				print "ERROR:::::%s"%(e)
				print "some Error"
				self.db.rollback()
		else:pass


		return item

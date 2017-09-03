# -*- coding: utf-8 -*-
# import MySQLdb
import psycopg2
class amazonDB():
	def __init__(self):
		# self.dbb = MySQLdb.connect("localhost","root","laptrip0","madstream")
		self.dbb = psycopg2.connect(database="crawler", user="root", password="crawler4218", host="crawler.cvyhh9zncx9e.ap-southeast-1.rds.amazonaws.com", port="5432")



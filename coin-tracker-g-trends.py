import pyodbc
import requests
import json
import time
import os
import matplotlib.pyplot as plt
import glob
import pytrends
from pytrends.request import TrendReq

def roundStr(numberToRound):
	return "{:.4f}".format(numberToRound) 
	
def loadConfig(filename):
	config = open(filename)
	data = json.load(config)
	return data

def GenerateTrends():
	print("Fetching Google Trends...", end="", flush=True)

	dbConfig = loadConfig('C:\AppCredentials\CoinTrackerPython\database.config')
	
	con = pyodbc.connect(dbConfig[0]["sql_conn"])
	cursor = con.cursor()
	
	cursor.execute("select name, id, symbol from CoinTracker.dbo.Market where id in (select coin_fk from CoinTracker.dbo.MarketHistory) and rank = 1 order by id")
	rows = cursor.fetchall()

	if cursor.rowcount == 0:
		print("No Price sources found")
		return;
		
	pytrends = TrendReq(hl='en-US', tz=360)

	for row in rows:
		kw_list = [str(row[0]),str(row[1])]
		pytrends.build_payload(kw_list)
		interest_over_time_df = pytrends.interest_over_time()
		print(interest_over_time_df)
		'''
		

		interest_by_region_df = pytrend.interest_by_region()

		print(interest_by_region_df.head())

		related_queries_dict = pytrend.related_queries()

		print(related_queries_dict)
		trending_searches_df = pytrend.trending_searches()

		print(trending_searches_df.head())

		top_charts_df = pytrend.top_charts(cid='actors', date=201611)

		print(top_charts_df.head())

		suggestions_dict = pytrend.suggestions(keyword='pizza')

		print(suggestions_dict)'''
	print("Done")

def main():
	GenerateTrends()

main()




__author__ = 'troyconant'

import MySQLdb
import mysql.connector
from mysql.connector import errorcode
import json
from pprint import pprint as pp

# From collected Groupon JSON files from the Web Scraper, this script connects to a MySQL database,
# parses and inserts Groupon records into DB. Transformtion/manipulation is then implemented to clean raw JSON data from Groupon.


with open('GOODS_sample_groupon_page_data_montana1.json') as json_deals:
    groupon_deals_json = json.load(json_deals)
    json_deals.close()

print len(groupon_deals_json)
print pp(groupon_deals_json)

select_deals = groupon_deals_json
print pp(select_deals)


# Connect to MySQL database in Amazon EC2 instance.
try:
insightful_database_connecting = mysql.connector.connect(user='troy', password='',
                                                         host='',
                                                         database='groupon')
                                                         
except mysql.connector.connect.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Error with Authentication"
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print "DATABASE DOES NOT EXIST"
	else:
		print "Error"
else:
insightful_database_connecting.close()
groupon_cursor = insightful_database_connecting.cursor()


# Setting up INSERT statment for db.

insert_statement = (
    """INSERT INTO groupon.goods_db (title, time_retrieved, amount_sold, amount_sold_2, url, discount, discount_2, groupon_price, groupon_price_2, retail_price, retail_price_2, categories, categories_2, categories_3, active,city) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")



# Transforms & Cleans incoming JSON records.

for eachmem in select_deals:
    for eachrow in eachmem:
        if eachrow.has_key('amount_sold'):
            if isinstance(eachrow['amount_sold'], list):
                amount_sold = eachrow['amount_sold'][0]
                amount_sold_2 = eachrow['amount_sold'][1]
            else:
                amount_sold = eachrow['amount_sold']
                amount_sold_2 = 'null'
        else:
            amount_sold = 'null'
            amount_sold_2 = 'null'

        if eachrow.has_key('groupon_price'):
            if isinstance(eachrow['groupon_price'], list):
                groupon_price = eachrow['groupon_price'][0]
                groupon_price_2 = eachrow['groupon_price'][1]
            else:
                groupon_price = eachrow['groupon_price']
                groupon_price_2 = 'null'
        else:
            groupon_price = 'null'
            groupon_price_2 = 'null'

        if eachrow.has_key('retail_price'):
            if isinstance(eachrow['retail_price'], list):
                retail_price = eachrow['retail_price'][0]
                retail_price_2 = eachrow['retail_price'][1]
            else:
                retail_price = eachrow['retail_price']
                retail_price_2 = 'null'
        else:
            retail_price = 'null'
            retail_price_2 = 'null'

        if eachrow.has_key('categories/_text'):
            if isinstance(eachrow['categories/_text'], list):
                if len(eachrow['categories/_text']) == 3:
                    categories = eachrow['categories/_text'][0]
                    categories_2 = eachrow['categories/_text'][1]
                    categories_3 = eachrow['categories/_text'][2]
                else:
                    categories = eachrow['categories/_text'][0]
                    categories_2 = eachrow['categories/_text'][1]
                    categories_3 = 'null'
            else:
                categories = eachrow['categories/_text']
                categories_2 = 'null'
                categories_3 = 'null'
        else:
            categories = 'null'
            categories_2 = 'null'
            categories_3 = 'null'

        if eachrow.has_key('discount'):
            discount = eachrow['discount']
            discount_2 = 'null'

        elif eachrow.has_key('retail_price'):
            discount = int(
                ((eachrow['retail_price'][0] - eachrow['groupon_price'][0]) / float(eachrow['retail_price'][0])) * 100)
            discount_2 = int(
                ((eachrow['retail_price'][1] - eachrow['groupon_price'][1]) / float(eachrow['retail_price'][1])) * 100)
        else:
            discount = 'null'
            discount = 'null'

        if eachrow.has_key('title'):
            title = eachrow['title']
        else:
            title = 'null'
        if eachrow.has_key('time_retrieved'):
            time_retrieved = eachrow['time_retrieved']
        else:
            time_retrieved = 'null'

        if eachrow.has_key('url'):
            url = eachrow['url']
        else:
            url = 'null'

        city = eachrow['city']

        if retail_price == retail_price_2 == groupon_price == discount:
            active = 'No'
        else:
            active = "Yes"

    deal_data = (
        title, time_retrieved, amount_sold, amount_sold_2, url, discount, discount_2, groupon_price, groupon_price_2,
        retail_price, retail_price_2, categories, categories_2, categories_3, active, city)

groupon_cursor.execute(insert_statement, deal_data)
insightful_database_connecting.commit()

groupon_cursor.close()
insightful_database_connecting.close()

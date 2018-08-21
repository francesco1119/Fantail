#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# We import the requests module which allows us to make the API call
import requests
import argparse
import pyodbc																		# Transfer data straight into Microsoft SQL Server
import sys
import json
import time
import datetime
from time import gmtime, strftime
import colorama
colorama.init()

# Here we organize the choices command line aruments 							
parser = argparse.ArgumentParser()													
parser.add_argument('--country', dest='country', type=str, help="input a country code (like \"US\" or \"FR\" or \"NZ\"), or \"ALL\" for all countries", metavar='') # Option: --country
parser.add_argument('--city', dest='city', 		type=str, help= "enter a city name (like \"New York\" or \"Paris\" or \"Auckland\")", metavar='')					# Option: --city
parser.add_argument('--category', dest='category', default='movie_theater', type=str, help="enter a business category",	metavar='')									# Option: --category
parser.add_argument('--radius', dest='radius', default='10000', type=int, help="enter a radius between 0 and 50000 (default is 10000)",	metavar='')					# Option: --radius
parser.add_argument('--speed', dest='speed', default='3', type=int, help="enter the number in seconds of speed (default is 3 seconds)",	metavar='')					# Option: --radius								
parser.add_argument('--do', dest='do', default='show', type=str, choices=['show', 'save'], help="arguments are \"show\" or \"save\"", metavar='')					# Option: --do		
parser.add_argument('--rownumber', dest='rownumber', type=int, help="input a specific row number", metavar='') 														# Option: --rownumber
args = parser.parse_args()
# If user directory nothing print help
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)
# Argparse ends here

# Terminal color definitions
class fg:
	BLACK   = '\033[30m'
	RED     = '\033[31m'
	GREEN   = '\033[32m'
	YELLOW  = '\033[33m'
	BLUE    = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN    = '\033[36m'
	WHITE   = '\033[37m'
	RESET   = '\033[39m'

class bg:
	BLACK   = '\033[40m'
	RED     = '\033[41m'
	GREEN   = '\033[42m'
	YELLOW  = '\033[43m'
	BLUE    = '\033[44m'
	MAGENTA = '\033[45m'
	CYAN    = '\033[46m'
	WHITE   = '\033[47m'
	RESET   = '\033[49m'

class style:
	BRIGHT    = '\033[1m'
	DIM       = '\033[2m'
	NORMAL    = '\033[22m'
	RESET_ALL = '\033[0m'

#####################################################################
# Enter here your Google Places API key								#
MyGooglePlacesAPIKey = 'MyBeautifulAPIKey'	#
																	#
# Enter here your database credentials 								#
Connection_Details = ('DRIVER={SQL Server};'						#
					  'SERVER=ASPIRES3;'							#
					  'DATABASE=ip2location;'						#
					  'UID=sqlninja;'								#
					  'PWD=sqlninja')								#
#####################################################################

long_field = {}
short_field = {}
url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
url2 = 'https://maps.googleapis.com/maps/api/place/details/json?'
#url_next = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=%s&key=%s' % (next_page_token, api_key)
next_page_token = ""
	
Total_Places_Found = 0
# GET all Places for a certain Latitude and Longitude
def GET_Places_for_Lat_Lon(url1):
	global page_no
	global response_data1
	url = url1  				
	params1 = {'location': '%s,%s' % (latitude,longitude),                                   
		      'radius': '%s' % (args.radius),												
		      'type': '%s' % (args.category),
		      'key': MyGooglePlacesAPIKey}														
	response1 = requests.get(url = url1, params=params1)															
	response_data1 = response1.json()
	#page_no += 1
	page_no = 0
# GET all details for a single Place_ID
def GET_Single_Place_Details(url2):
	
	global response_data2
	url = url2  				
	params2 = {'placeid': SQL_Place_ID,                                   
			'key': MyGooglePlacesAPIKey}														
	response2 = requests.get(url = url2, params=params2)															
	response_data2 = response2.json()

def Google_call_for_details():
	
	global Googleplace_id
	global Googleid
	global GoogleName
	global GoogleStreet_Number
	global GoogleStreet
	global GooglePostal_Code
	global GoogleCity
	global GoogleArea1
	global GoogleArea2
	global GoogleCountry
	global GoogleCountryCode
	global GooglePhone
	global GoogleLatitude
	global GoogleLongitude
	global GoogleTypes
	global GoogleRating
	global GoogleURL
	global GoogleWebsite
	

	GET_Single_Place_Details(url2)	
	
	if response_data2['status'] == 'OK':
		Googleplace_id = response_data2['result'].get("place_id", None)
		Googleid = response_data2['result'].get("id", None)
		GoogleName = response_data2['result'].get("name", None)
		for e in response_data2['result']['address_components']:
			for t in e['types']:
				long_field[t] = e['long_name']
				short_field[t] = e['short_name']
				GoogleStreet_Number = long_field.get("street_number", None)
				GoogleStreet = long_field.get("route", None)
				GooglePostal_Code = long_field.get("postal_code", None)
				GoogleCity = long_field.get("locality", None)
				GoogleArea1 = long_field.get("administrative_area_level_1", None)
				GoogleArea2 = long_field.get("administrative_area_level_2", None)
				GoogleCountry = long_field.get("country", None)
				GoogleCountryCode = short_field.get("country", None)
		GooglePhone = response_data2['result'].get("international_phone_number", None)
		GoogleLatitude = response_data2['result']['geometry']['location'].get("lat", None)
		GoogleLongitude = response_data2['result']['geometry']['location'].get("lng", None)
		GoogleRating = response_data2['result'].get("rating", None)
		GoogleTypes = json.dumps(response_data2['result']['types'])
		GoogleURL = response_data2['result'].get("url", None)
		GoogleWebsite = response_data2['result'].get("website", None)
		time.sleep(args.speed)
  
def get_place_for(countdown_order,latitude, longitude,city_name,country_code,url1):                                                      
	
	global SQL_Place_ID
	global next_page_token
	global Place_found
	global page_no
		
	global Total_Places_Found
	
	connection2 = pyodbc.connect(Connection_Details)										
	cursor2 = connection2.cursor()

	connection3 = pyodbc.connect(Connection_Details)										
	cursor3 = connection3.cursor()	
	
	Place_found = 0
	
	
	
	GET_Places_for_Lat_Lon(url1)
	
	sqlStatement = 	"""
					INSERT INTO GoogleDetails (	Place_ID,
												ID,
												Name,
												Street_Number,
												Street,
												Postal_Code,
												City,
												Area1,
												Area2,
												Country,
												CountryCode,
												Phone,
												Latitude,
												Longitude,
												Types,
												Rating,
												GoogleURL,
												Website
												) 
					values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
					""" 
	# Here we go to store JSON elements for SQL
	
	if response_data1['status'] == 'ZERO_RESULTS':
		print (fg.RED,style.BRIGHT + '{0}) Nothing found for: {1}, {2} at {3}'.format(countdown_order,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),style.RESET_ALL))
		time.sleep(args.speed)
	
	if response_data1['status'] == 'OVER_QUERY_LIMIT':
		while response_data1['status'] == 'OVER_QUERY_LIMIT':
			print (fg.RED,style.BRIGHT +'{0}) OVER_QUERY_LIMIT for: {1}, {2} at {3}. I will try again in 1 hour.'.format(countdown_order,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),style.RESET_ALL))
			time.sleep(3600)
			get_place_for(countdown_order,latitude, longitude,city_name,country_code,url1)
	
	elif response_data1['status'] == 'OK':
		Total_Places_Found += len(response_data1['results'])

		for SQL_element in response_data1['results']:
			SQL_Place_ID = SQL_element['place_id']
			SQL_Latitude = SQL_element['geometry']['location']['lat']
			SQL_Longitude = SQL_element['geometry']['location']['lng']
			
			if args.do == 'show':
				Google_call_for_details()
				print (fg.GREEN,style.BRIGHT + '+' + style.RESET_ALL,GoogleName,':',GoogleStreet_Number,GoogleStreet,', ',GoogleCity,GoogleCountryCode,'(',GoogleLatitude,',',GoogleLongitude,')')			
			
			elif args.do == 'save':
				sqlStatementPlace_ID = 	"""
										select Place_ID 
										from GoogleDetails 
										where Place_ID = '%s'
										""" % (SQL_Place_ID)
				cursor3.execute(sqlStatementPlace_ID)
				row = cursor3.fetchone()
				if row == None:
					Google_call_for_details()
				else:
					continue
			
				cursor2.execute(sqlStatement, \
								Googleplace_id, \
								Googleid, \
								GoogleName, \
								GoogleStreet_Number, \
								GoogleStreet, \
								GooglePostal_Code, \
								GoogleCity, \
								GoogleArea1, \
								GoogleArea2, \
								GoogleCountry, \
								GoogleCountryCode, \
								GooglePhone, \
								GoogleLatitude, \
								GoogleLongitude, \
								GoogleTypes, \
								GoogleRating, \
								GoogleURL, \
								GoogleWebsite)
				connection2.commit()
			
				Place_found += 1			
			else:
				pass				
			
		#Next_page_token
		#test next_page_token
		
		if 'next_page_token' in response_data1:
			#page_no += 1
			next_page_token = response_data1['next_page_token']
			print (fg.GREEN,style.BRIGHT +' On page number', page_no, 'found:', len(response_data1['results']),'places',style.RESET_ALL)
			url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=%s&key=%s' % (next_page_token, MyGooglePlacesAPIKey)
			get_place_for(countdown_order,latitude, longitude,city_name,country_code,url1)
			
		else:
			#page_no += 1
			print (fg.GREEN,style.BRIGHT +' On page number', page_no, ',', 'found:', len(response_data1['results']),'places',style.RESET_ALL)
	page_no += 1	
	#Print_Total(countdown_order,latitude, longitude,city_name,country_code,Place_found,page_no,Total_Places_Found)
	time.sleep(args.speed)
	
def Print_Total(countdown_order,latitude, longitude,city_name,country_code,Place_found,page_no,Total_Places_Found): 
	if args.do == 'show':
		print (fg.GREEN,style.BRIGHT + '{0}) Total Places found: {1} near: {2}, {3} at {4}'.format(countdown_order,Total_Places_Found,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),style.RESET_ALL))

	elif args.do == 'save':
		if Place_found == 0:
			print (fg.YELLOW,style.BRIGHT +'{0}) Places found {1}, but Places saved {2} (all already in database) near: {3}, {4} at {5}'.format(countdown_order,Total_Places_Found,Place_found,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),style.RESET_ALL))
			time.sleep(args.speed)
		else:
			print (fg.GREEN,style.BRIGHT +'{0}) Places found {1}, Places saved {2} near: {3}, {4} at {5}'.format(countdown_order,Total_Places_Found,Place_found,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),style.RESET_ALL))
			time.sleep(args.speed)	
			
def SQLQuery():

	global latitude
	global longitude

	# We connect to SQL Server Management Studio
	connection = pyodbc.connect(Connection_Details)											
	cursor = connection.cursor()
	
	if args.country:
		sqlStatement = 	"""
						SELECT 
						ROW_NUMBER() OVER (ORDER BY country_code desc,city_name desc) as countdown_order,
						AVG(latitude) AS latitude, 
						AVG(longitude) AS longitude, 
						city_name, 
						country_code
						FROM ip2location_db11
						where country_code = '%s'
						GROUP BY country_code, city_name
						ORDER BY country_code, city_name 	
						""" % (args.country) 
	if args.country == "ALL":
		sqlStatement =  """
						SELECT 
						ROW_NUMBER() OVER (ORDER BY country_code desc,city_name desc) as countdown_order,
						AVG(latitude) AS latitude, 
						AVG(longitude) AS longitude, 
						city_name, 
						country_code
						FROM ip2location_db11
						GROUP BY country_code, city_name
						ORDER BY country_code, city_name
						""" 
	if args.city: 
		sqlStatement = 	"""
						SELECT 
						ROW_NUMBER() OVER (ORDER BY country_code desc,city_name desc) as countdown_order,
						AVG(latitude) AS latitude, 
						AVG(longitude) AS longitude, 
						city_name, 
						country_code
						FROM ip2location_db11
						where city_name = '%s'
						GROUP BY country_code, city_name
						ORDER BY country_code, city_name 
						""" % (args.city)
	if args.country and args.rownumber:
		sqlStatement = 	"""
						SELECT *
						FROM
						(	SELECT 
							ROW_NUMBER() OVER (ORDER BY country_code desc, 
							city_name desc) as countdown_order,
							AVG(latitude) AS latitude, 
							AVG(longitude) AS longitude, 
							city_name, 
							country_code   
							FROM  ip2location_db11 
							where country_code = '%s'
							GROUP BY country_code, city_name
						) as D
						where countdown_order < %s
						ORDER BY country_code, city_name 	
						""" % (args.country,args.rownumber)
	if args.country and args.city:
		sqlStatement = 	"""
						WITH cte AS
						(   SELECT *, ROW_NUMBER() OVER (PARTITION BY latitude, longitude ORDER BY latitude, longitude) AS rn,
							DENSE_RANK() OVER (ORDER BY city_name desc) as countdown_order
							FROM ip2location_db11
							where country_code = '%s'
							and city_name = '%s'
						)
						SELECT countdown_order,latitude,longitude,city_name,country_code
						FROM cte
						WHERE rn = 1
						order by city_name 		
						""" % (args.country,args.city)
		
	try:	
		cursor.execute(sqlStatement)
		
		for countdown_order, latitude, longitude,city_name,country_code in cursor:
			get_place_for(countdown_order, latitude, longitude,city_name,country_code,url1)
			Print_Total(countdown_order,latitude, longitude,city_name,country_code,Place_found,page_no,Total_Places_Found)
			
	finally:
		cursor.close()
		connection.close()  
SQLQuery()

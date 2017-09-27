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
from colorama import init
init(autoreset=True)
from fabric.colors import red, green

# Here we organize the choices command line aruments 							
parser = argparse.ArgumentParser()													
parser.add_argument('--country', dest='country', 			 						# Option: --country
					type=str, 
					help="input a country code (like \"US\" or \"FR\" or \"NZ\")", 
					metavar='') 
parser.add_argument('--city', dest='city', 											# Option: --city
					type=str, 
					help= "enter a city name (like \"New York\" or \"Paris\" or \"Auckland\")",	
					metavar='')
parser.add_argument('--category', dest='category', 
					default='movie_theater',										# Option: --category
					type=str, 
					help="enter a business category",	
					metavar='')	
parser.add_argument('--radius', dest='radius', 
					default='25000',												# Option: --radius
					type=int, 
					help="enter a radius between 0 and 50000 (default is 25000)", 
					metavar='')					
parser.add_argument('--do', dest='do', 
					default='show',													# Option: --do
					type=str, 
					choices=['show', 'save'], 
					help="arguments are \"show\" or \"save\"", 
					metavar='')			# Option: --SQL statement 
parser.add_argument('--rownumber', dest='rownumber', 			 					# Option: --country
					type=int, 
					help="input a specific row number", 
					metavar='') 
args = parser.parse_args()

#####################################################################
# Enter here your Google Places API key								#
MyGooglePlacesAPIKey = 'AIzaSyDnfdcHa3n7iDzi_NqZ0sXslC1KmAiGZdQ'	#
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

  
def get_place_for_show(countdown_order,latitude, longitude,city_name,country_code):	
	
	#Google call for Place_ID                                                                            
	url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'	 				
	params1 = {'location': '%s,%s' % (latitude,longitude),                                   
		      'radius': '%s' % (args.radius),												
		      'type': '%s' % (args.category),
		      'key': MyGooglePlacesAPIKey}														
	response1 = requests.get(url = url1, params=params1)															
	response_data1 = response1.json()	
	
	# Here we go to store JSON elements for SQL	
	if response_data1['status'] == 'ZERO_RESULTS':
		print ("\033[91m"+'{0}) Nothing found for: {1}, {2} at {3}'.format(countdown_order,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m"))
		time.sleep(2)
		
	elif response_data1['status'] == 'OK':
		for SQL_element in response_data1['results']:
			SQL_Place_ID = SQL_element['place_id']
			
			url2 = 'https://maps.googleapis.com/maps/api/place/details/json?'	 				
			params2 = {'placeid': SQL_Place_ID,                                   
					'key': 'AIzaSyDnfdcHa3n7iDzi_NqZ0sXslC1KmAiGZdQ'}														
			response2 = requests.get(url = url2, params=params2)															
			response_data2 = response2.json()		
			
			if response_data2['status'] == 'OK':
#				Googleplace_id = response_data2['result'].get("place_id", None)
#				Googleid = response_data2['result'].get("id", None)
				GoogleName = response_data2['result'].get("name", None)
				for e in response_data2['result']['address_components']:
					for t in e['types']:
						long_field[t] = e['long_name']
						short_field[t] = e['short_name']
						GoogleStreet_Number = long_field.get("street_number", None)
						GoogleStreet = long_field.get("route", None)
#						GooglePostal_Code = long_field.get("postal_code", None)
						GoogleCity = long_field.get("locality", None)
#						GoogleArea1 = long_field.get("administrative_area_level_1", None)
#						GoogleArea2 = long_field.get("administrative_area_level_2", None)
#						GoogleCountry = long_field.get("country", None)
						GoogleCountryCode = short_field.get("country", None)
#				GooglePhone = response_data2['result'].get("international_phone_number", None)
				GoogleLatitude = response_data2['result']['geometry']['location'].get("lat", None)
				GoogleLongitude = response_data2['result']['geometry']['location'].get("lng", None)
#				GoogleRating = response_data2['result'].get("rating", None)
#				GoogleTypes = json.dumps(response_data2['result']['types'])
#				GoogleURL = response_data2['result'].get("url", None)
#				GoogleWebsite = response_data2['result'].get("website", None)
				time.sleep(2)
							
			print ("\033[92m"+'+'+"\033[0m",GoogleName+':',GoogleStreet_Number,GoogleStreet,', ',GoogleCity,GoogleCountryCode,'(',GoogleLatitude,',',GoogleLongitude,')')
			
		#Next_page_token
		
		print ("\033[92m"+'{0}) Total Places found: {1} near: {2}, {3} at {4}'.format(countdown_order,len(response_data1['results']),city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m"))
		time.sleep(2)

	
	elif response_data1['status'] == 'OVER_QUERY_LIMIT':
		while response_data1['status'] == 'OVER_QUERY_LIMIT':
			#print ("\033[91m" +'OVER_QUERY_LIMIT for:',countdown_order,')',city_name,',',country_code,'at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m")
			print ("\033[91m"+'{0}) OVER_QUERY_LIMIT for: {1}, {2} at {3}. I will try again in 15 minutes.'.format(countdown_order,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m"))
			time.sleep(900)

def get_place_for_save(countdown_order,latitude, longitude,city_name,country_code):                                                      
	
	connection2 = pyodbc.connect(Connection_Details)										
	cursor2 = connection2.cursor()

	connection3 = pyodbc.connect(Connection_Details)										
	cursor3 = connection3.cursor()

	Place_found = 0
	
	#Google call for Place_ID                                                                            
	url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'	 				
	params1 = {'location': '%s,%s' % (latitude,longitude),                                   
		      'radius': '%s' % (args.radius),												
		      'type': '%s' % (args.category),
		      'key': MyGooglePlacesAPIKey}														
	response1 = requests.get(url = url1, params=params1)															
	response_data1 = response1.json()	
	
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
	#while True:
	#	try:
	if response_data1['status'] == 'ZERO_RESULTS':
		print ("\033[91m"+'{0}) Nothing found for: {1}, {2} at {3}'.format(countdown_order,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m"))
		time.sleep(2)
		
	elif response_data1['status'] == 'OK':
		for SQL_element in response_data1['results']:
			SQL_Place_ID = SQL_element['place_id']
			
			sqlStatementPlace_ID = 	"""
									select Place_ID 
									from GoogleDetails 
									where Place_ID = '%s'
									""" % (SQL_Place_ID)
			cursor3.execute(sqlStatementPlace_ID)
			row = cursor3.fetchone()
			if row == None:
	
				#Google call for Details
				url2 = 'https://maps.googleapis.com/maps/api/place/details/json?'	 				
				params2 = {'placeid': SQL_Place_ID,                                   
						'key': 'AIzaSyDnfdcHa3n7iDzi_NqZ0sXslC1KmAiGZdQ'}														
				response2 = requests.get(url = url2, params=params2)															
				response_data2 = response2.json()		
				
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
					time.sleep(2)
					
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
		
		if Place_found == 0:
			print ("\033[93m"+'{0}) Places found {1}, but Places saved {2} (all already in database) near: {3}, {4} at {5}'.format(countdown_order,len(response_data1['results']),Place_found,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m"))
			time.sleep(2)
		else:
			print ("\033[92m"+'{0}) Places found {1}, Places saved {2} near: {3}, {4} at {5}'.format(countdown_order,len(response_data1['results']),Place_found,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m"))
			time.sleep(2)
	
	elif response_data1['status'] == 'OVER_QUERY_LIMIT':
		while response_data1['status'] == 'OVER_QUERY_LIMIT':
			print ("\033[91m"+'{0}) OVER_QUERY_LIMIT for: {1}, {2} at {3}. I will try again in 15 minutes.'.format(countdown_order,city_name,country_code,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"\033[0m"))
			time.sleep(30)
					
def SQLQuery():
	# We connect to SQL Server Management Studio
	connection = pyodbc.connect(Connection_Details)											
	cursor = connection.cursor()
	
	if args.country:
		sqlStatement = 	"""
						WITH cte AS
						(   SELECT *, ROW_NUMBER() OVER (PARTITION BY latitude, longitude ORDER BY latitude, longitude) AS rn,
							DENSE_RANK() OVER (ORDER BY city_name desc) as countdown_order
							FROM ip2location_db11
							where country_code = '%s'
						)
						SELECT countdown_order,latitude,longitude,city_name,country_code
						FROM cte
						WHERE rn = 1
						order by city_name 	
						""" % (args.country) 
	#elif args.country == "ALL":
	#	sqlStatement = "select latitude,longitude,city_name,country_code from ip2location_db11 order by country_name,city_name" 
	elif args.city: 
		sqlStatement = 	"""
						WITH cte AS
						(   SELECT *, ROW_NUMBER() OVER (PARTITION BY latitude, longitude ORDER BY latitude, longitude) AS rn,
							DENSE_RANK() OVER (ORDER BY city_name desc) as countdown_order
							FROM ip2location_db11
							where city_name = '%s'
						)
						SELECT countdown_order,latitude,longitude,city_name,country_code
						FROM cte
						WHERE rn = 1
						order by city_name 
						""" % (args.city)
	if args.country and args.rownumber:
		sqlStatement = 	"""
						WITH cte AS
						(   SELECT *, ROW_NUMBER() OVER (PARTITION BY latitude, longitude ORDER BY latitude, longitude) AS rn,
							DENSE_RANK() OVER (ORDER BY city_name desc) as countdown_order
							FROM ip2location_db11
							where country_code = '%s'
						)
						SELECT countdown_order,latitude,longitude,city_name,country_code
						FROM cte
						WHERE rn = 1
						and countdown_order <= '%s'
						order by city_name 	
						""" % (args.country,args.rownumber) 
		
	try:	
		cursor.execute(sqlStatement)
		
		for countdown_order, latitude, longitude,city_name,country_code in cursor:
			if args.do == 'show':
				get_place_for_show(countdown_order, latitude, longitude,city_name,country_code)
			if args.do == 'save':
				get_place_for_save(countdown_order, latitude, longitude,city_name,country_code)
	finally:
		cursor.close()
		connection.close()  
SQLQuery()
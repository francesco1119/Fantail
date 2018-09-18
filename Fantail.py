#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import googlemaps
import json
import argparse
import sys
import pyodbc
import time
import datetime
import colorama
colorama.init()
from moneyed import Money	

# Here we organize the choices command line aruments 							
parser = argparse.ArgumentParser()													
parser.add_argument('--country', dest='country', type=str, help="input a country code (like \"US\" or \"FR\" or \"NZ\"), or \"ALL\" for all countries", metavar='') # Option: --country
parser.add_argument('--city', dest='city', 		type=str, help= "enter a city name (like \"New York\" or \"Paris\" or \"Auckland\")", metavar='')					# Option: --city
parser.add_argument('--category', dest='category', default='movie_theater', type=str, help="enter a business category",	metavar='')									# Option: --category
parser.add_argument('--radius', dest='radius', default='10000', type=int, help="enter a radius between 0 and 50000 (default is 10000)",	metavar='')					# Option: --radius
parser.add_argument('--verbose', dest='verbose',help='Print more data',action='store_true')																# Option: --verbose		
parser.add_argument('--rownumber', dest='rownumber', type=int, help="input a specific row number", metavar='') 														# Option: --rownumber
args = parser.parse_args()
# If user directory nothing print help
#if len(sys.argv) < 2:
#    parser.print_help()
#    sys.exit(1)
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

	
#############################################################################
# Enter here your Google Places API key										#
gmaps = googlemaps.Client(key='MyBeautifulAPIKey')	#
																			#
# Enter here your database credentials 										#
Connection_Details = ('DRIVER={SQL Server};'								#
					  'SERVER=ASPIRES3;'									#
					  'DATABASE=ip2location;'								#
					  'UID=sqlninja;'										#
					  'PWD=sqlninja')										#
#############################################################################

long_field = {}
short_field = {}
element_count = 0
element_saved = 0
Total_cost = Money(amount='0.00', currency='USD')


def Search_URL(countdown_order,latitude, longitude,city_name,region_name,country_code):
	
	global search_location
	global params
	global Total_cost

	params = {'location': '%s,%s' % (latitude,longitude),
				'radius': '%s' % (args.radius),
				'type': '%s' % (args.category)
				}
	
	search_location = gmaps.places_nearby(**params)
	Total_cost += Money(amount='0.01', currency='USD')
	if search_location['status'] == 'OK':														# Check if the API is 'OK'
		nearby_search(search_location)
	elif search_location['status'] == 'ZERO_RESULTS':
		pass
		#print_totals(countdown_order,city_name,region_name,country_code)
	else:
		print ('API query returned:',search_location)

def nearby_search(search_location):
	
	global element_count
	global Place_ID
	global ID
	global Name
	global Latitude
	global Longitude
	global Rating
	global Types
	global Vicinity
	global Total_cost
	
	for element in search_location['results']:
		Place_ID = element.get('place_id',None)
		ID = element.get('id',None)
		Name = element.get('name',None)
		Latitude = element['geometry']['location'].get('lat',None)
		Longitude = element['geometry']['location'].get('lng',None)
		Rating = element.get('rating',None)
		Types = json.dumps(element.get('types',None))		# Genius!
		Vicinity = element.get('vicinity',None)
		if 'next_page_token' in search_location.keys(): 
			time.sleep(5)
			params.update({"page_token": search_location['next_page_token']})
			search_location = gmaps.places_nearby(**params)
			Total_cost += Money(amount='0.01', currency='USD')
			nearby_search(search_location)
		
		Search_if_Place_ID_exists(Place_ID,ID,Name,Latitude,Longitude,Rating,Types,Vicinity)
		element_count += 1

	#return element
		
def Search_if_Place_ID_exists(Place_ID,ID,Name,Latitude,Longitude,Rating,Types,Vicinity):
	
	global element_saved
	
	cnxn = pyodbc.connect(Connection_Details)
	CursorSearch = cnxn.cursor()
	sqlSearchPlace_ID = 	"""
							select Place_ID 
							from GoogleNearbySearch 
							where Place_ID = '%s'
							""" % (Place_ID)
	CursorSearch.execute(sqlSearchPlace_ID)
	row = CursorSearch.fetchone()
	if row == None:
		element_saved += 1
		save_to_mssql(Place_ID,ID,Name,Latitude,Longitude,Rating,Types,Vicinity)
		Search_For_Place_ID(Place_ID)
		if args.verbose:
			print (fg.GREEN,style.BRIGHT,Name,style.RESET_ALL,":",Vicinity)
	else: 
		if args.verbose:
			print (fg.YELLOW,style.BRIGHT,Name,style.RESET_ALL,":",Vicinity)
		pass
	
	return element_saved

def save_to_mssql(Place_ID,ID,Name,Latitude,Longitude,Rating,Types,Vicinity):

	cnxn_nearby_search = pyodbc.connect(Connection_Details)
	CursorSearch = cnxn_nearby_search.cursor()
	SQLCommand = 	"""
					INSERT INTO GoogleNearbySearch (
													Place_ID,
													ID,
													Name,
													Latitude,
													Longitude,
													Rating,
													Types,
													Vicinity
													) 
					values (?,?,?,?,?,?,?,?)
					"""
	Values = [Place_ID,ID,Name,Latitude,Longitude,Rating,Types,Vicinity]
	
	CursorSearch.execute(SQLCommand, Values)
	cnxn_nearby_search.commit()

def Search_For_Place_ID(Place_ID):
	
	global Total_cost
	
	params = {'place_id': Place_ID}
	search_detials = gmaps.place(**params)
	Total_cost += Money(amount='0.01', currency='USD')
	
	if search_detials['status'] == 'OK':														# Check if the API is 'OK'
		Search_Details(search_detials)
	else:
		print ('API *details* query returned:',search_detials)
	
def Search_Details(search_detials):
	
	Googleplace_id = search_detials['result'].get("place_id", None)
	Googleid = search_detials['result'].get("id", None)
	GoogleName = search_detials['result'].get("name", None)
	for e in search_detials['result']['address_components']:
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
	GooglePhone = search_detials['result'].get("international_phone_number", None)
	GoogleLatitude = search_detials['result']['geometry']['location'].get("lat", None)
	GoogleLongitude = search_detials['result']['geometry']['location'].get("lng", None)
	GoogleRating = search_detials['result'].get("rating", None)
	GoogleTypes = json.dumps(search_detials['result']['types'])									# genius!
	GoogleURL = search_detials['result'].get("url", None)
	GoogleWebsite = search_detials['result'].get("website", None)
	
	Save_Place_Details(Googleplace_id,Googleid,GoogleName,GoogleStreet_Number,GoogleStreet,GooglePostal_Code,GoogleCity,GoogleArea1,GoogleArea2,GoogleCountry,GoogleCountryCode,GooglePhone,GoogleLatitude,GoogleLongitude,GoogleTypes,GoogleRating,GoogleURL,GoogleWebsite)
	
def Save_Place_Details(Googleplace_id,Googleid,GoogleName,GoogleStreet_Number,GoogleStreet,GooglePostal_Code,GoogleCity,GoogleArea1,GoogleArea2,GoogleCountry,GoogleCountryCode,GooglePhone,GoogleLatitude,GoogleLongitude,GoogleTypes,GoogleRating,GoogleURL,GoogleWebsite):
	
	# We connect to SQL Server Management Studio
	connection_details = pyodbc.connect(Connection_Details)											
	#cursor = connection.cursor()
	CursorSaveDetails = connection_details.cursor()

	SQL_Save_Details = 	"""
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
	
	CursorSaveDetails.execute(SQL_Save_Details, \
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
	connection_details.commit()
	
def print_totals(countdown_order, city_name,region_name,country_code):
	global element_count
	global element_saved
	
	if element_count == 0:
		print (fg.RED,style.BRIGHT,countdown_order,")","Total places found1:",element_count,",","saved:",element_saved,"in",city_name,",",region_name,",",country_code,Total_cost,"(",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),")",style.RESET_ALL)
	else:
		if element_count != 0 and element_count == element_saved:
			print (fg.GREEN,style.BRIGHT,countdown_order,")","Total places found2:",element_count,",","saved:",element_saved,"in",city_name,",",region_name,",",country_code,Total_cost,"(",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),")",style.RESET_ALL)
		elif element_count > element_saved:
			print (fg.YELLOW,style.BRIGHT,countdown_order,")","Total places found3:",element_count,",","saved:",element_saved,"in",city_name,",",region_name,",",country_code,Total_cost,"(",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),")",style.RESET_ALL)
	element_count = 0
	element_saved = 0
	
def SQLQuery():

	global latitude
	global longitude

	# We connect to SQL Server Management Studio
	connection = pyodbc.connect(Connection_Details)											
	#cursor = connection.cursor()
	CursorSearchLatLon = connection.cursor()
	
	if args.country:
		sqlStatement = 	"""
						SELECT 
						ROW_NUMBER() OVER (ORDER BY country_code desc,city_name desc) as countdown_order,
						AVG(latitude) AS latitude, 
						AVG(longitude) AS longitude, 
						city_name,
						region_name, 
						country_code						
						FROM ip2location_db11
						where country_code = '%s'
						GROUP BY country_code, region_name, city_name
						ORDER BY country_code, city_name 	
						""" % (args.country) 
	if args.country == "ALL":
		sqlStatement =  """
						SELECT 
						ROW_NUMBER() OVER (ORDER BY country_code desc,city_name desc) as countdown_order,
						AVG(latitude) AS latitude, 
						AVG(longitude) AS longitude, 
						city_name, 
						region_name,
						country_code						
						FROM ip2location_db11
						GROUP BY country_code, region_name, city_name
						ORDER BY country_code, city_name
						""" 
	if args.city: 
		sqlStatement = 	"""
						SELECT 
						ROW_NUMBER() OVER (ORDER BY country_code desc,city_name desc) as countdown_order,
						AVG(latitude) AS latitude, 
						AVG(longitude) AS longitude, 
						city_name, 
						region_name,
						country_code						
						FROM ip2location_db11
						where city_name = '%s'
						GROUP BY country_code, region_name, city_name
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
							region_name,
							country_code						
							FROM  ip2location_db11 
							where country_code = '%s'
							GROUP BY country_code, region_name, city_name
						) as D
						where countdown_order < %s
						ORDER BY country_code, city_name 	
						""" % (args.country,args.rownumber)
	if args.country and args.city:
		sqlStatement = 	"""
						SELECT 
						ROW_NUMBER() OVER (ORDER BY country_code desc,city_name desc) as countdown_order,
						AVG(latitude) AS latitude, 
						AVG(longitude) AS longitude, 
						city_name, 
						region_name,
						country_code						
						FROM ip2location_db11
						where country_code = '%s'
						and city_name = '%s'
						GROUP BY country_code, region_name, city_name
						ORDER BY country_code, city_name		
						""" % (args.country,args.city)
		
	try:	
		CursorSearchLatLon.execute(sqlStatement)
		
		for countdown_order, latitude, longitude,city_name,region_name,country_code in CursorSearchLatLon:
			Search_URL(countdown_order,latitude, longitude,city_name,region_name,country_code)
			print_totals(countdown_order, city_name,region_name,country_code)
	finally:
		CursorSearchLatLon.close()
		connection.close()  
SQLQuery()

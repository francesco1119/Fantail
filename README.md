<p align="center">
![alt text](http://www.ngamanuimages.org.nz/images/lres/d03689.jpg)
<p align="center">
[![GitHub issues](https://img.shields.io/github/issues/francesco1119/Fantail.svg)](https://github.com/francesco1119/Fantail/issues)
[![GitHub forks](https://img.shields.io/github/forks/francesco1119/Fantail.svg)](https://github.com/francesco1119/Fantail/network)
[![GitHub stars](https://img.shields.io/github/stars/francesco1119/Fantail.svg)](https://github.com/francesco1119/Fantail/stargazers)
[![GitHub license](https://img.shields.io/github/license/francesco1119/Fantail.svg)](https://github.com/francesco1119/Fantail/blob/master/LICENSE)
</p>
</p>
## Fantail
#### Fantail is a native New Zealand bird. 
#### Fantail is also a Python script that will scrap Google Places API for you without crap and will save the results in a SQL Server Database 

How to Install
======

1) Download and install DB11 (IP2Location™ LITE IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE Database) from [here](https://http://lite.ip2location.com/database/ip-country-region-city-latitude-longitude-zipcode-timezone), follow the instruction on the same download page and you will have the DB imported into SQL Server in a minute. 
2) Then install `pip install googlemaps json argparse pyodbc time datetime colorama decimal`
3) Download the query `SQLQuery_Create_Fantai_Details_Table.sql` and run it against your IP2location database: 2 tables will be created and there Fantail will store your precious data 
4) Configure ODBC to connect to Microsoft SQL Server (help yourself [following this guide](https://www.youtube.com/watch?v=tUiaK5fRH7k&ab_channel=itgeared))
5) Now open `Fantail.py` and insert your Google Places API into the variable `gmaps` and your ODBC credentials into the variable `Connection_Details`

```
#############################################################################
# Enter here your Google Places API key						#
gmaps = googlemaps.Client(key='MyBeautifulAPIKey')	#
										#
# Enter here your database credentials 						#
Connection_Details = ('DRIVER={SQL Server};'					#
					  'SERVER=ASPIRES3;'			#
					  'DATABASE=ip2location;'		#
					  'UID=sqlninja;'			#
					  'PWD=sqlninja')			#
#############################################################################
```

How to use it 
------

Because life is hard enought I did the best I could to develop someting that just works. 
Well, the code is horrible but it get the job done....
You don't have to write not even 1 line of code; so sit down and relax because I'm going to feed you with a spoon.

Try you run `python Fantail.py --help` and you will see:
```
usage: Fantail.py [-h] [--country] [--city] [--category] [--radius]
                  [--verbose] [--rownumber]

optional arguments:
  -h, --help    show this help message and exit
  --country     Input a country code (like "US" or "FR" or "NZ"), or "ALL" for all countries
  --city        Enter a city name (like "New York" or "Paris" or "Auckland")
  --category    Enter a business category
  --radius      Enter a radius between 0 and 50000 (default is 10000)
  --verbose     Print more data
  --rownumber   Input a specific row number 
  ```

Pretty easy to understand how to use it, right?

![New_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/New.PNG)

Open an Issue if you have any question.

How it works under the hood 
------

The world is quite big to scrap using random geographical coordinates. You need to avoid oceans, deserts, jungles, lakes, mountain chains and plces where simply there is nothing. Google provides you 25,000 query search per day but you will run out of query if you search where there is nothing. So I based the search on IP2Location™, a database that stores the coordinates of IP adresses. 

So in **Australia** you will search just on are where there are human beings, avoiding to search in the middle of the desert:
![Australia_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/Australia.PNG)

While in **Switzerland** you will avoid so waste your precious queries into the Lake of Geneva or in remote places in the Alps (as you can see ther e are a few dots in the Alps so, don't worry, small villages are counted in)
![Switzerland_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/Swiss.PNG)

**France** is copletely covered as it has a lot of IP 
![France_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/France.PNG)

**Kazakhstan** has less but I'm quite sure there are no commerce listed on Google Places for remote areas without internet access (Please, kazakhs friends, don't take this personal, I've never been to Kazakhstan but from Google Maps I couldn't find many commerces for remote areas and I choose your country as an example. I know for sure there are cinemas, hospitals, restaruants, etc... I'm just saying that Google Map doesn't list them . If I'm telling bulshit just drop me a line and I will correct this phrase.)
![Kazakhstan_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/Kazakhstan.PNG)

You don't want to search for a restaurant in the middle of the **Brazilian** jungle, right? (alright, now, if you find a restaurant in the middle of the Brazilian jungle and is listed on Google Maps, please drop me a line because I want to visit it)
![Brazil_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/Brazil.PNG)

Limitations
------

Fantail doesn't search for geographic area like this:

![Fantail_Not](https://github.com/francesco1119/Fantail/blob/master/images/whatnot.png)

If you want to do so [go here](https://iliauk.com/2015/12/18/data-mining-google-places-cafe-nero-example/)

Future developent
------
On spare time my TODO list is:

* add "find" search

**Please if you have requests drop me a line**

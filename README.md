## Fantail
#### Fantail will scrap Google Places API for you and will save the results in a SQL Server Database 
![alt text](http://www.ngamanuimages.org.nz/images/lres/d03689.jpg)

How to Install
======

1) Download and install DB11 (IP2Location™ LITE IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE Database) from [here](https://http://lite.ip2location.com/database/ip-country-region-city-latitude-longitude-zipcode-timezone), follow the instruction on the same download page and you will have the DB imported into SQL Server in a minute. 
2) Then install `pip install requests argparse pyodbc json time datetime colorama fabric colors`
3) Download the query `SQLQuery_Create_Fantai_Details_Table.sql` and run it against your IP2location database: a table will be created and there Fantail will store your precious data  

How to use it 
------

Because life is hard enought I did the best I could to develop someting that just works. 
Well, the code is horrible but it get the job done....
You don't have to write not even 1 line of code; sit down and relax because I'm going to feed you with a spoon. 
* `python Fantail.py --help` will print all the options for you 
* `python Fantail.py --city "Auckland" --category "hospital"` will return all the hospitals in Auckland. Look [here for a complete list of categories](https://developers.google.com/places/supported_types) supported bu Google Places API.
* `python Fantail.py --country "NZ" --category "hospital"` will return all hospitals in New Zealand (so put "US" for United States, "FR" for France, etc...)
* `python Fantail.py --country "NZ" --category "hospital" --do "save"` will start saving the results in your SQL Server database. 

Limitations
------


### Fantail
Fantail will scrap Google Places API for you and will save the results in a SQL Server Database 
![alt text](http://www.ngamanuimages.org.nz/images/lres/d03689.jpg)

How to Install
======

1) Download and install DB11 (IP2Location™ LITE IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE Database) from [here](https://http://lite.ip2location.com/database/ip-country-region-city-latitude-longitude-zipcode-timezone), follow the instruction on the same download page and you will have the DB imported into SQL Server in a minute. 
2) Then install `pip install requests argparse pyodbc json time datetime colorama fabric colors`
3) Download the query `SQLQuery_Create_Fantai_Details_lTable.sql` and run it against your ip2location database: a table will be created and there Fantail will store your precious data  

Alt-H2
------


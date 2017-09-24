## Fantail
#### Fantail is a native New Zealand bird. 
#### Fantail is also a Python script that will scrap Google Places API for you without crap and will save the results in a SQL Server Database 
![alt text](http://www.ngamanuimages.org.nz/images/lres/d03689.jpg)

How to Install
======

1) Download and install DB11 (IP2Location™ LITE IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE Database) from [here](https://http://lite.ip2location.com/database/ip-country-region-city-latitude-longitude-zipcode-timezone), follow the instruction on the same download page and you will have the DB imported into SQL Server in a minute. 
2) Then install `pip install requests argparse pyodbc json time datetime colorama fabric colors`
3) Download the query `SQLQuery_Create_Fantai_Details_Table.sql` and run it against your IP2location database: a table will be created and there Fantail will store your precious data 
4) Configure ODBC to connect to Microsoft SQL Server (help yourself [following this guide](https://www.youtube.com/watch?v=tUiaK5fRH7k&ab_channel=itgeared))
5) Now open `Fantail.py` and insert your Google Places API into the variable `MyGooglePlacesAPIKey` and your ODBC credentials into the variable `Connection_Details`

How to use it 
------

Because life is hard enought I did the best I could to develop someting that just works. 
Well, the code is horrible but it get the job done....
You don't have to write not even 1 line of code; so sit down and relax because I'm going to feed you with a spoon. 
* `python Fantail.py --help` will print all the options for you 
* `python Fantail.py --city "Auckland" --category "hospital"` will return all the hospitals in Auckland. Look [here for a complete list of categories](https://developers.google.com/places/supported_types) supported bu Google Places API.
* `python Fantail.py --city "Auckland" --category "hospital" --radius "1000"` will limit the radius research to 1000 around your target. By default the radius research is set to 25,000; you can push it till 50,000
* `python Fantail.py --country "NZ" --category "hospital"` will return all hospitals in New Zealand (so put "US" for United States, "FR" for France, etc...)
* `python Fantail.py --country "NZ" --category "hospital" --do "save"` will start saving the results in your SQL Server database. 

How it works under the hood 
------

The world is quite big to scrap using random geographical coordinates. You need to avoid oceans, deserts, jungles, lakes, mountain chains and plces where simply there is nothing. Google provides you 25,000 query search per day but you will run out of query if you search where there is nothing. So I based the search on IP2Location™, a database that stores the coordinates of IP adresses. 

So in **Australia** you will search just on are where there are human beings, avoiding to search in the middle of the desert:
![Australia_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/Australia.PNG)

While in **Switzerland** you will avoid so waste your precious queries into the Lake of Geneva or in remote places in the Alps (as you can see ther e are a few dots in the Alps so, don't worry, small villages are counted in)
![Switzerland_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/Swiss.PNG)

**France** is copletely covered as it has a lot of IP 
![France_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/France.PNG)

**Kazakhstan** has less but I'm quite sure there are no commerce listed on Google Places for remote areas without internet access 
![Kazakhstan_Fantail](https://github.com/francesco1119/Fantail/blob/master/images/Kazakhstan.PNG)


Future developent
------
I will try to mantain this repository but if I don't have time, please fork this

# Hikr

Hikr is an application that provides integrated collaborative planning tools.
It allows users to create hiking trips, add members, share information, communicate, 
share trip route points and general details about the trip. 

# Table of Content

  - Technologies Used
  - How to locally run Hikr
  - How to use Hiker

### Technologies Used

* [Python] 
* [Flask] 
* [PostgreSQL/PostGIS] 
* [SQLAlchemy]
* [Javascript/jQuery] 
* [AJAX/JSON]
* [SocketIO]
* [Flask SocketIO]
* [AngularJS]
* [Jinja2] 
* [Twitter Bootstrap]
* [OpenStreetMap (OSM) Dataset]
* [Osm2pgsql]
* [Google Maps API] 
 (dependencies are listed in requirements.txt)

### How to locally run Hikr

Hikr has not yet been deployed, so here is how to run the app locally on your machine.

#### How to Obtain Trail Data

Some of Hikr maping features (trails and elevation profile) depend on dataset obtained from Open Street Map. For this version of the app, trail data is obtained for California alone. To be able to use these features of the app, please follow the following steps to setup local OSM PostreSQL database:
* To obtain dataset for California, download california-latest.osm.pbf from http://download.geofabrik.de/north-america/us/california.html
* Install osm2pgsql for Ubuntu. For instructions on other operating systems please check out osm2pgsql page.
   ```sh
   apt-get install osm2pgsql
   ```
* Install osmosis for Ubuntu. For instructions on other operating systems please check out http://wiki.openstreetmap.org/wiki/Osmosis/Installation#Linux
   ```sh
   apt-get install osmosis
   ```
* Follow the commands below to create database for highways alone:
    ```sh
    osmosis --read-pbf california-latest.osm.pbf \
    --tf accept-ways highway=* --used-node \
    --wb california-hiking.osm.pbf
    ```
* Create database gis using the following commands:
    ```sh
    createdb gis
    psql -d gis -c 'CREATE EXTENSION postgis; CREATE EXTENSION hstore;'
    osm2pgsql -l -c -d gis --slim -C 1000 --flat-nodes california-hiking.osm.pbf
    ```
* After these steps the OSM database is set up and should be ready to use after following the steps below.
    
#### Run Hiker Flask App

* Set up and activate a python virtualenv, and install all dependencies:
    ```sh
    pip install -r requirements.txt
    ```
* Make sure you have PostgreSQL running. Create a new database in psql named hiker:
    ```sh
    createdb hiker
    ```
* Create the tables in your database:
   ```sh
    python -i model.py
    db.create_all()
    quit()
    python seed.py
    ```
* Start up flask server:
    ```sh
    python server.py
    ```
* Go to localhost:5000 to interact with the app

### How to use Hikr
*   Create an account on the registration page
*   Once account is created, you will be routed to your user page 
*   To create new trip click on the "Create New Trip"
*   Input trip information and click "Submit". You will be routed to the trip page
*   On the trip page you can add members to the trip by using a drop-down list of users with their names and user names listed
*   You can create new trips by clicking the Create New Trip link. 
*   You can add action items by clicking on the To-Do-List and save by clicking Submit.
*   You can use the messaging app to send messages to all members in your trip
*   To create a route you can search the trailhead on the search window and click "Search" button to pan the map to the area
*   Your map will be loaded with trails (colorcoded) in the area you searched and a list of the trails with trailnames will be displayed in the right hand side of the map. 
*   You can click on any trail and you will be able to see an elevation profile for that trail.
*   You can double click on the map to create a marker 
*   To add note on marker you can right click to add a comment and "Update" to save your comment
*   Once all markers for your route have been added, click "Log This Route" to save your trip information.
*   All data entered for the trip will be saved next time you login and visit the trip page.

### Author

Blerina Aliaj is an Electrical Engineer entering the world of Software Engineering.

[//]: # (These are reference links used in the body of this note)

   [Python]: <https://www.python.org/>
   [Flask]: <http://flask.pocoo.org/>
   [PostgreSQL/PostGIS]: <https://www.postgresql.org/>
   [SQLAlchemy]: <http://www.sqlalchemy.org/>
   [Javascript/jQuery]: <http://jquery.com>
   [AJAX/JSON]: <http://ace.ajax.org>
   [SocketIO]: <https://socket.io/>
   [Flask SocketIO]: <https://flask-socketio.readthedocs.io/en/latest/>
   [AngularJS]: <https://angularjs.org/>
   [Jinja2]: <http://jinja.pocoo.org/>
   [Twitter Bootstrap]: <http://getbootstrap.com/2.3.2/>
   [OpenStreetMap (OSM) Dataset]: <https://en.wikipedia.org/wiki/OpenStreetMap>
   [Osm2pgsql]: <http://wiki.openstreetmap.org/wiki/Osm2pgsql>
   [Google Maps API]: <https://developers.google.com/maps/>



  

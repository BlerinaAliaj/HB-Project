# Hiker

Hiker is an application that provides integrated collaborative planning tools.
It allows users to create hiking trips, add members, share information, communicate, 
share trip route points and general details about the trip. 

# Table of Content

  - Technologies Used
  - How to locally run Hiker
  - How to use Hiker

### Technologies Used

* [Python] 
* [Flask] 
* [PostgresSQL/PostGIS] 
* [SQLAlchemy]
* [Javascript/jQuery] 
* [AJAX/JSON] 
* [Jinja2] 
* [Google Maps API] 
 (dependencies are listed in requirements.txt)

### How to locally run Hiker

Hiker has not yet been deployed, so here is how to run the app locally on your machine.

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

### How to use Hiker
*   Create an account on the registration page
*   Once account is created, you will be routed to your user page 
*   To create new trip click on the "Create New Trip"
*   Input trip information and click "Submit". You will be routed to the user profile page
*   On the profile page you will see the new trip has been listed. 
*   Click on the trip and you will be routed to the trip page
*   On the trip page you can add members to the trip by their user ID
*   You can use the messaging app to send messages to all members in your trip
*   You can add action items regarding your trip to the list
*   To create a route you can search the trailhead on the search window and click "Geocode" button to pan the map to the area
*   You can double click on the map to create a marker 
*   To add note on marker you can right click to add a comment and "Update" to save your comment
*   Once all markers for your route have been added, click "Log This Route" to save your trip information.
*   All data entered for the trip will be saved next time you login and visit the trip page.

### Author

Blerina Aliaj is an Electrical Engineer entering the world of Software Engineering.

[//]: # (These are reference links used in the body of this note)

   [Python]: <https://www.python.org/>
   [Flask]: <http://flask.pocoo.org/>
   [PostgresSQL/PostGIS]: <https://www.postgresql.org/>
   [SQLAlchemy]: <http://www.sqlalchemy.org/>
   [Javascript/jQuery]: <http://jquery.com>
   [AJAX/JSON]: <http://ace.ajax.org>
   [Jinja2]: <http://jinja.pocoo.org/>
   [Google Maps API]: <https://developers.google.com/maps/>



  

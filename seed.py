"""Utility file to seed database from map data and seed some artificial user and trip data. 

This file is under construction....

"""

from sqlalchemy import func
from model import User
from model import Trip
from model import UserTrip
from model import Geodata
from model import Comment

from model import connect_to_db, db
from server import app

import datetime




# def load_geodata():
#     """Load geodata from mapping data into database."""

#     print "Geodata"

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     User.query.delete()

#     # Read file and insert data
#     for row in open("seed_data/u.user"):
#         row = row.rstrip()
#         user_id, age, gender, occupation, zipcode = row.split("|")

#         user = User(user_id=user_id,
#                     age=age,
#                     zipcode=zipcode)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(user)

#     # Once we're done, we should commit our work
#     db.session.commit()

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # # If table isn't empty, empty it
    # Cat.query.delete()

    # Add Users
    alain = User(user_id='eagle5', first_name='Alain', last_name='Rodriguez',
                 email='eagle5@gmail.com', password='alain', zipcode='94115')
    sofiane = User(user_id='souali', first_name='Sofiane', last_name='Ouali',
                 email='sofiane@gmail.com', password='sofiane', zipcode='94116')
    henry = User(user_id='hlin', first_name='Henry', last_name='Lin',
                 email='henry@gmail.com', password='henry', zipcode='94117')

    # Add Trips
    yos = Trip(trip_code='yos0', trip_name='Yosemite Winter Backpacking',
                    date_created=datetime.datetime.now())
    bv = Trip(trip_code='bear0', trip_name='Bear Valley Winter Backpacking',
                    date_created=datetime.datetime.now())
    kc = Trip(trip_code='king0', trip_name='King Canyon Summer Backpacking',
                    date_created=datetime.datetime.now())

    trip1 = UserTrip(trip_code='yos0', user_id='eagle5')
    trip2 = UserTrip(trip_code='bear0', user_id='eagle5')
    trip3 = UserTrip(trip_code='king0', user_id='eagle5')

    trip4 = UserTrip(trip_code='yos0', user_id='souali')
    trip5 = UserTrip(trip_code='bear0', user_id='souali')
    trip6 = UserTrip(trip_code='king0', user_id='souali')

    trip7 = UserTrip(trip_code='yos0', user_id='hlin')
    trip8 = UserTrip(trip_code='bear0', user_id='hlin')
    trip9 = UserTrip(trip_code='king0', user_id='hlin')

    mess1 = Comment(trip_code='yos0', user_id='eagle5', comment="We should take my car",
                    time=datetime.datetime.now())
    mess2 = Comment(trip_code='yos0', user_id='hlin', comment="Great idea!!!!",
                    time=datetime.datetime.now())
    mess3 = Comment(trip_code='yos0', user_id='souali', comment="Who's driving?",
                    time=datetime.datetime.now())


    # Add new objects to session, so they'll persist
    db.session.add(alain)
    db.session.add(sofiane)
    db.session.add(henry)
    db.session.add(yos)
    db.session.add(bv)
    db.session.add(kc)
    db.session.commit()
    db.session.add(trip1)
    db.session.add(trip2)
    db.session.add(trip3)
    db.session.add(trip4)
    db.session.add(trip5)
    db.session.add(trip6)
    db.session.add(trip7)
    db.session.add(trip8)
    db.session.add(trip9)

    db.session.commit()
    db.session.add(mess1)
    db.session.add(mess2)
    db.session.add(mess3)

    db.session.commit()


    # Import different types of data
    # load_geodata()
    # set_val_user_id()

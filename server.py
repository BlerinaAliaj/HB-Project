"""Hiker App"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from model import User, Trip, UserTrip, Comment, CheckList, Geodata, GeodataTrip, Route, connect_to_db, db
import datetime
from flask_socketio import SocketIO, send, emit, join_room
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "wonderwall"

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

# Create connection to my 'gis' database

gis_db = create_engine('postgresql:///gis')
GISSession = sessionmaker(gis_db)


@app.route('/')
def index():
    """Homepage."""

    if "user" in session:
        return redirect("/profile")

    return render_template("homepage.html")


@app.route('/login', methods=["GET"])
def login_page():
    """Page that asks users for login information"""

    if "user" in session:
        return redirect("/profile")

    return render_template("homepage.html")


@app.route('/login', methods=["POST"])
def login():
    """Verifies that user login exists."""

    username = request.form.get('username')
    password = request.form.get('password')

    query_user = User.query.filter_by(user_id=username).first()

    if query_user:
        user_pass = query_user.password

        if password == user_pass:
            # We add user id and password to sessions user dictionary
            session["user"] = query_user.user_id

            # Query trips so it redirects to the most recent trip
            query = User.query.get(session["user"])

            # query trips and show them in reverse chronological order
            trips = query.trips
            sorted_trips = sorted(trips, key=lambda x: x.date_created, reverse=True)

            trip_code = sorted_trips[0].trip_code

            flash('You have successfully logged in.')
            return redirect("/trip_detail/"+trip_code)

        else:
            flash("Your username and password are not correct.")
            return render_template("homepage.html")

    else:
        flash("""Sorry, that username doesn't exist. Please try again or go to
            registration page to register new account""")
        return redirect("/login")


@app.route('/register', methods=["GET"])
def register_page():
    """Page that asks users for login information"""

    if "user" in session:
        return redirect("/profile")

    return render_template("register.html")


@app.route('/register', methods=["POST"])
def register():
    """Sends user to registration page."""

    username = request.form.get('username')
    print "my username is %s" % username
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')
    zipcode = request.form.get('zipcode')

    query_user = User.query.filter_by(user_id=username).first()

    if not query_user:
        user = User(user_id=username, first_name=firstname, last_name=lastname,
                    email=email, password=password, zipcode=zipcode)
        db.session.add(user)
        db.session.commit()
        session['user'] = username

    else:
        flash("""That username is already taken. Please choose another one or
            go to login page""")
        return redirect("/register")

    # return redirect('/')
    return redirect('/profile')


@app.route('/profile')
def user_detail():
    """User detail page"""

    if 'user' in session:
        # profile page will have content based on the user logged-in
        username = session['user']

        # Query user by their username
        query_user = User.query.get(username)
        name = query_user.first_name

        # query trips and show them in reverse chronological order
        trips = query_user.trips
        # use the sorted built-in function with lamda function where the key
        # we are using to sort by is the date trip was created. Will reverse
        # list to show latest trip first
        sorted_trips = sorted(trips, key=lambda x: x.date_created, reverse=True)



        return render_template("user_profile.html", user_id=username, name=name,
                                trips=sorted_trips)
    else:
        flash("You are not logged in. Please do so")
        return redirect('/')


@app.route('/logout')
def logout():
    """Logs out user"""

    del session["user"]
    flash("You have been successfully logged out.")

    return redirect('/')


@app.route('/member_profile/<user_id>')
def display_friend_info(user_id):
    """ This page will display all info for other members of your group """

    pass


# @app.route('/new_trip', methods=["GET"])
# def get_trip_data():
#     """Template to create new trip"""

#     if 'user' in session:
#         return render_template("new_trip.html")
#     else:
#         flash("You are not logged in. Please do so.")
#         return redirect('/')


@app.route('/new_trip', methods=["POST"])
def create_trip():
    """Route that will log new trip information to database"""

    if 'user' in session:
        username = session['user']
        trip_name = request.form.get('tripname')
        date_created = datetime.datetime.now()
        date_start = request.form.get('datestart')
        num_days = int(request.form.get('numdays'))

        # Generate trip code here:
        trip_abbr = trip_name[:4].lower()
        query_trips = Trip.query.all()

        for trip in query_trips:
            if trip.trip_code[:4] == trip_abbr:

                appx = int(trip.trip_code[4:])
                appx += 1
                trip_code = trip_abbr + format(appx, "03")
                # print trip_code
                break
            else:
                trip_code = trip_abbr + "000"

        # write new trip object to database:
        new_trip = Trip(trip_code=trip_code, trip_name=trip_name, date_created=date_created,
                       date_start=date_start, num_days=num_days)
        new_trip_log = UserTrip(trip_code=trip_code, user_id=username)

        # add trip objects to database and commit
        db.session.add(new_trip)
        db.session.commit()
        db.session.add(new_trip_log)
        db.session.commit()

        return json.dumps({'status': 'ok', 'user': username, 'tripCode': trip_code})

    else:
        flash("You are not logged in. Please do so.")
        return redirect('/')


@app.route('/trip_detail/<trip_code>')
def trip_detail(trip_code):
    """Page that displays all information about the trip."""

    if 'user' in session:
        # get username from session
        username = session['user']

        # Start quering all information for the trip page
        query_user = User.query.get(username)
        query_trip = Trip.query.get(trip_code)
        query_list = CheckList.query.filter_by(trip_code=trip_code).order_by(CheckList.item_id)

        # Query present user name and trip name
        name = query_user.first_name
        trip_name = query_trip.trip_name

        # Query all other members for the group
        members = Trip.query.get(trip_code).users

        # Query Lists:
        items = query_list.all()

        # query comment
        query_comment = Comment.query.filter_by(trip_code=trip_code)
        comments = query_comment.all()
        sorted_messages = sorted(comments, key=lambda x: x.time, reverse=True)

        # query trips and show them in reverse chronological order
        trips = query_user.trips

        # use the sorted built-in function with lamda function where the key
        # we are using to sort by is the date trip was created. Will reverse
        # list to show latest trip first
        sorted_trips = sorted(trips, key=lambda x: x.date_created, reverse=True)

        trip_date = query_trip.date_start.strftime("%B %d, %Y")
        trip_length = query_trip.num_days
        trip_loc = query_trip.start_loc

        return render_template('trip_detail.html', username=username, name=name,
                    trip_name=trip_name, members=members, trips=sorted_trips,
                    trip_code=trip_code, items=items, messages=comments,
                    trip_date=trip_date, trip_length=trip_length, trip_loc=trip_loc)
    else:
        flash("You are not logged in. Please do so.")
        return redirect('/')


@app.route('/list_trips')
def list_trips():
    """Returns list of all trips"""

    if 'user' in session:
        # get username from session
        username = session['user']

    query_user = User.query.get(username)

    # query trips and show them in reverse chronological order
    trips = query_user.trips
    sorted_trips = sorted(trips, key=lambda x: x.date_created, reverse=True)

    my_json = {}
    my_json['trips'] = []

    for trip in sorted_trips:
        my_json['trips'].append({'trip_name': trip.trip_name,
                                 'trip_code': trip.trip_code,
                                 })
    # print my_json
    return json.dumps(my_json)


@socketio.on('join')
def on_join(room):
    join_room(room)

    print 'joined room %s' % room

    user_name = session['user']
    # print user_name
    emit('message', user_name + ' has entered the room.', room=room)


@socketio.on('json')
def handleMessage(msg):
    """This uses sockeio to receive a message object from client (input text)
    with message and room. Writes message to database table and sends the
    message back to client
    """
    # print ('Message: ' + msg)

    username = session['user']

    # print msg['room']
    # print username

    my_message = Comment(trip_code=msg['room'], user_id=username, comment=msg["msg"],
                         time=datetime.datetime.now())
    db.session.add(my_message)
    db.session.commit()

    # emit('message', msg['msg'], room=msg['room'])
    send(msg['msg'], room=msg['room'])


@app.route('/list.json', methods=["GET"])
def get_list_items():

    trip_code = request.headers.get('trip_code')
    print "my trip code is %s" % trip_code

    query_list = CheckList.query.filter_by(trip_code=trip_code).order_by(CheckList.item_id)
    # Query Lists:
    items = query_list.all()

    # Query members for that trip
    members = UserTrip.query.filter_by(trip_code=trip_code).all()
    member_list = []

    for member in members:
        member_list.append((member.user.first_name, member.user_id))
        

    print member_list

    my_json = {}
    my_json['items'] = []
    my_json['users'] = member_list
    print my_json

    for item in items:
        my_json['items'].append({'item_id': item.item_id,
                                 'trip_code': item.trip_code,
                                 'userid': item.user_id,
                                 'description': item.description,
                                 'selected': item.completed})
    print json.dumps(my_json)
    return json.dumps(my_json)


@app.route('/list.json', methods=["POST"])
def add_to_list():
    """Reads items from database. Adds items to list table"""

    all_data = json.loads(request.data)
    trip_code = all_data['tripCode']

    print "list trip code is %s" % trip_code

    data = json.loads(all_data['data'])

    new_data = json.loads(all_data['newdata'])

    print data
    print new_data

    for key in data:
        # We check to see if key is in database table and rewrite the values
        user_id = key["userid"]
        list_item = key["description"]
        completed = key["completed"]
        item_id = key['list_id']

        # query list for the list id
        query_list = CheckList.query.get(item_id)

        query_list.user_id = user_id
        query_list.description = list_item
        query_list.completed = completed
        db.session.commit()

    for key in new_data:
        # We write new items to database
        user_id = key["userid"]
        list_item = key["description"]
        completed = key["completed"]

        if list_item != "" and user_id != "":

            my_list = CheckList(trip_code=trip_code, user_id=user_id, description=list_item,
                        completed=completed)

            db.session.add(my_list)
            db.session.commit()

    query_data = CheckList.query.filter_by(trip_code=trip_code).all()

    my_json = {}
    my_json['items'] = []

    for item in query_data:
        my_json['items'].append({'item_id': item.item_id,
                                 'trip_code': item.trip_code,
                                 'userid': item.user_id,
                                 'description': item.description,
                                 'selected': item.completed})

    return json.dumps(my_json)


@app.route('/add_member/<trip_code>', methods=["GET"])
def add_members_form(trip_code):
    """Option to add members to trip"""

    username = session['user']
    user_set = set()

    # Query all users for the trip
    query_users = UserTrip.query.filter(UserTrip.trip_code == trip_code).all()

    for user in query_users:
        user_set.add(user.user_id)
        print "user ID : %s" % user.user_id

    # get users that don't have that trip code
    all_users = User.query.all()


    return render_template("add_member.html", users=all_users, user_set=user_set,
                            trip_code=trip_code)


@app.route('/add_member/<trip_code>', methods=["POST"])
def add_members(trip_code):
    """Add members to trip """

    user_id = request.form.get("memberid")
    print "user ID: %s" % user_id

    new_member = UserTrip(trip_code=trip_code, user_id=user_id)
    db.session.add(new_member)
    db.session.commit()

    return redirect("/trip_detail/"+trip_code)


@app.route('/add_marker.json/<trip_code>')
def load_markers(trip_code):
    """Uploads markers if they exist to map"""

    query_routes = Route.query.filter_by(trip_code=trip_code).all()
    routes = {}

    for route in query_routes:
        routes[route.route_id] = {"lng": route.lon,
                                  "lat": route.lat,
                                  "description": route.description}

    return jsonify(routes)


@app.route('/add_marker.json', methods=["POST"])
def add_marker_data():
    """Gets the marker data and writes them to tables in database """

    content = request.form.get('data')
    my_markers = json.loads(content)
    trip_code = request.form.get('trip_code')

    search_trip = Route.query.filter_by(trip_code=trip_code).all()
    # print search_trip

    if search_trip:
        for trip in search_trip:
            # print trip
            db.session.delete(trip)
            db.session.commit()

    for key in my_markers:
        # print key
        lat = my_markers[key]['lat']
        lon = my_markers[key]['lng']
        desc = my_markers[key].get('marker_description', None)

        marker = Route(trip_code=trip_code, lon=lon, lat=lat, description=desc)
        db.session.add(marker)
        db.session.commit()

    return redirect("/trip_detail/"+trip_code)


@app.route('/query_osm.json')
def query_osm_on_viewport():
    """Queries osm databased based on viewport, returns all ways within the viewport"""

    # Creates separate database session for 'gis' database
    gis_session = GISSession()

    latNE = request.args.get('latNE')
    lngNE = request.args.get('lngNE')
    latSW = request.args.get('latSW')
    lngSW = request.args.get('lngSW')

    sql = """SELECT osm_id, name, ST_AsGeoJSON(way) AS geo_json
                FROM planet_osm_line
                    WHERE (
                        way && ST_MakeEnvelope(:lngSW, :latSW, :lngNE, :latNE, 4326)
                        OR
                        way ~ ST_MakeEnvelope(:lngSW, :latSW, :lngNE, :latNE, 4326)
                        OR 
                        way @ ST_MakeEnvelope(:lngSW, :latSW, :lngNE, :latNE, 4326)
                    ) """
             # UNION
             # SELECT osm_id, name, ST_AsGeoJSON(way) AS geo_json
             #    FROM planet_osm_roads
             #        WHERE (
             #            way && ST_MakeEnvelope(:lngSW, :latSW, :lngNE, :latNE, 4326)
             #            OR
             #            way ~ ST_MakeEnvelope(:lngSW, :latSW, :lngNE, :latNE, 4326)
             #            OR 
             #            way @ ST_MakeEnvelope(:lngSW, :latSW, :lngNE, :latNE, 4326)
             #        )

    all_nodes = gis_session.execute(sql, {'lngSW': lngSW,
                             'latSW': latSW,
                             'lngNE': lngNE,
                             'latNE': latNE})

    nodes = all_nodes.fetchall()

    # print nodes

    my_gis_data = {}

    for shape_id, trail_name, geo_json in nodes:
        if trail_name != None:
            my_gis_data[trail_name] = {
                'type': "Feature",
                'geometry': json.loads(geo_json),
                'properties': {
                    'window': [latNE, lngNE, latSW, lngSW],
                    'id': shape_id,
                    'name': trail_name
                }
            }

    return json.dumps(my_gis_data)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # app.run(port=5000, host='0.0.0.0')
    # for websockets use the socketio.run instead of app.run
    socketio.run(app, port=5000, host='0.0.0.0')

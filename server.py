"""Hiker App"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from model import User, Trip, UserTrip, Comment, CheckList, Geodata, GeodataTrip, Route, connect_to_db, db
import datetime
from flask_socketio import SocketIO, send, emit, join_room


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "wonderwall"

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


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

    return render_template("login.html")


@app.route('/login', methods=["POST"])
def login():
    """Verifies that user login exists."""

    username = request.form.get('username')
    password = request.form.get('password')
    # print username
    # print password

    query_user = User.query.filter_by(user_id=username).first()

    if query_user:
        user_pass = query_user.password

        if password == user_pass:
            # We add user id and password to sessions user dictionary
            session["user"] = query_user.user_id
            flash('You have successfully logged in.')
            return redirect("/profile")
            # return redirect('/user_detail/' + str(user_id))

        else:
            flash("Your username and password are not correct.")
            return render_template("login.html")

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


@app.route('/new_trip', methods=["GET"])
def get_trip_data():
    """Template to create new trip"""

    if 'user' in session:
        return render_template("new_trip.html")
    else:
        flash("You are not logged in. Please do so.")
        return redirect('/')


@app.route('/new_trip', methods=["POST"])
def create_trip():
    """Route that will log new trip information to database"""

    #To create new trip we need add to Trip and UserTrip to log everything in
    # Trip: trip_code, trip_name, date_created, date_start, start_loc, end_loc
    # num_days

    # UserTrip: trip_code, user_id

    if 'user' in session:
        username = session['user']
        # trip_code = request.form.get('tripcode')
        trip_name = request.form.get('tripname')
        date_created = datetime.datetime.now()
        date_start = request.form.get('datestart')
        # start_loc = request.form.get('startloc')
        # end_loc = request.form.get('endloc')
        num_days = int(request.form.get('numdays'))

        # Generate trip code here:
        trip_abbr = trip_name[:4].lower()
        print trip_abbr
        query_trips = Trip.query.all()

        for trip in query_trips:
            if trip.trip_code[:4] == trip_abbr:

                appx = int(trip.trip_code[4:])
                appx += 1
                trip_code = trip_abbr + format(appx, "03")
                print trip_code
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

        # return redirect('/profile')
        return json.dumps({'status': 'ok', 'user': username, 'tripCode': trip_code})
        # return redirect('/trip_detail/'+trip_code)
    else:
        flash("You are not logged in. Please do so.")
        return redirect('/')


@app.route('/trip_detail/<trip_code>')
def trip_detail(trip_code):
    """Page that displays all information about the trip.

    This is where all the cool stuff happens :)
    """
    #print trip_code
    # UserTrip: trip_code, user_id

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

        # add information for display in the webpage
        return render_template('trip_detail.html', username=username, name=name,
                    trip_name=trip_name, members=members,
                    trip_code=trip_code, items=items, messages=comments)
    else:
        flash("You are not logged in. Please do so.")
        return redirect('/')


# @app.route('/message.json/<trip_code>', methods=["GET"])
# def read_message(trip_code):
#     """Queries messages/comments table for all messages for that trip"""

#     query_comment = Comment.query.filter_by(trip_code=trip_code)
#     comments = query_comment.all()
#     sorted_messages = sorted(comments, key=lambda x: x.time, reverse=True)

#     messages = {}

#     for message in sorted_messages:
#         messages[message.comment_id] = {"message": message.comment,
#                                         "user": message.user_id,
#                                         "timestamp": message.time}

#     return jsonify(messages)


# @app.route('/message', methods=["POST"])
# def commit_message():
#     """Write messages to server """

#     username = session['user']
#     message = request.form.get("message")
#     trip_code = request.form.get("trip_code")

#     # Write message to database
#     my_message = Comment(trip_code=trip_code, user_id=username, comment=message,
#                          time=datetime.datetime.now())
#     db.session.add(my_message)
#     db.session.commit()
#     return redirect("/trip_detail/"+trip_code)

@socketio.on('join')
def on_join(room):
    join_room(room)

    print 'joined room %s' % room

    user_name = session['user']
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


@app.route('/list.json', methods=["POST"])
def add_to_list():
    """Adds items to list table"""

    trip_code = request.form.get('tripCode')
    print trip_code

    all_data = request.form.get('allData')
    data = json.loads(all_data)
    print all_data
    print data

    for key in data:
        if key == "addItem":
            # We write new items to database
            user_id = data[key]["userid"]
            list_item = data[key]["description"]
            completed = data[key]["completed"]
            print completed

            if not completed:
                completed = False

            if list_item and user_id: 

                my_list = CheckList(trip_code=trip_code, user_id=user_id, description=list_item,
                            completed=completed)

                db.session.add(my_list)
                db.session.commit()

        elif key != "header":
            # We check to see if key is in database table and rewrite the values
            user_id = data[key]["userid"]
            list_item = data[key]["description"]
            completed = data[key]["completed"]

            # query list for the list id
            query_list = CheckList.query.get(key)

            query_list.user_id = user_id
            query_list.description = list_item
            query_list.completed = completed
            db.session.commit()

    # return trip_code

    return redirect("/trip_detail/"+trip_code)





# @app.route('/list/<trip_code>', methods=["POST"])
# def add_to_list(trip_code):
#     """Adds items to list table"""

#     list_item = request.form.get("description")
#     print list_item
#     user_id = request.form.get("userid")
#     completed = request.form.get("completed")
#     if not completed:
#         completed = False

#     # Write list to database
#     my_list = CheckList(trip_code=trip_code, user_id=user_id, description=list_item,
#                         completed=completed)

#     db.session.add(my_list)
#     db.session.commit()
#     return redirect("/trip_detail/"+trip_code)


@app.route('/add_member/<trip_code>', methods=["GET"])
def add_members_form(trip_code):
    """Option to add members to trip"""

    username = session['user']
    user_set = set()

    # Query all users for the trip
    query_users = UserTrip.query.filter(UserTrip.trip_code == trip_code).all()

    for user in query_users:
        user_set.add(user.user_id)
        print user.user_id

    # get users that don't have that trip code
    all_users = User.query.all()


    return render_template("add_member.html", users=all_users, user_set=user_set,
                            trip_code=trip_code)


@app.route('/add_member/<trip_code>', methods=["POST"])
def add_members(trip_code):
    """Add members to trip """

    user_id = request.form.get("memberid")
    print user_id

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
    print search_trip

    if search_trip:
        for trip in search_trip:
            print trip
            db.session.delete(trip)
            db.session.commit()

    for key in my_markers:
        print key
        lat = my_markers[key]['lat']
        lon = my_markers[key]['lng']
        desc = my_markers[key].get('marker_description', None)

        marker = Route(trip_code=trip_code, lon=lon, lat=lat, description=desc)
        db.session.add(marker)
        db.session.commit()

    return redirect("/trip_detail/"+trip_code)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # app.run(port=5000, host='0.0.0.0')
    # for websockets use the socketio.run instead of app.run
    socketio.run(app, port=5000, host='0.0.0.0')

"""Hiker App"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
from model import User, Trip, UserTrip, Comment, List, Geodata, GeodataTrip, Route, connect_to_db, db
import datetime


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "wonderwall"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login', methods=["GET"])
def login_page():
    """Page that asks users for login information"""

    return render_template("login.html")


@app.route('/login', methods=["POST"])
def login():
    """Verifies that user login exists."""

    if "user" not in session:
        session["user"] = {}

    username = request.form.get('username')
    password = request.form.get('password')

    query_user = User.query.filter_by(user_id=username).first()

    if query_user:
        user_pass = query_user.password

        if password == user_pass:
            # We add user id and password to sessions user dictionary
            session["user"] = query_user.user_id
            user_id = query_user.user_id
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

    return render_template("register.html")


@app.route('/register', methods=["POST"])
def register():
    """Sends user to registration page."""

    username = request.form.get('username')
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
        trip_code = request.form.get('tripcode')
        trip_name = request.form.get('tripname')
        date_created = datetime.datetime.now()
        date_start = request.form.get('datestart')
        start_loc = request.form.get('startloc')
        end_loc = request.form.get('endloc')
        num_days = int(request.form.get('numdays'))

        # write new trip object to database:
        new_trip = Trip(trip_code=trip_code, trip_name=trip_name, date_created=date_created,
                       date_start=date_start, start_loc=start_loc, end_loc=end_loc,
                       num_days=num_days)
        new_trip_log = UserTrip(trip_code=trip_code, user_id=username)

        # add trip objects to database and commit
        db.session.add(new_trip)
        db.session.commit()
        db.session.add(new_trip_log)
        db.session.commit()

        # return redirect('/profile')
        return redirect('/trip_detail/'+trip_code)
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
        query_comment = Comment.query.filter_by(trip_code=trip_code)
        query_list = List.query.filter_by(trip_code=trip_code)

        # Query present user name and trip name
        name = query_user.first_name
        trip_name = query_trip.trip_name

        # Query all other members for the group
        members = Trip.query.get(trip_code).users

        # Query messages
        messages = query_comment.all()
        sorted_messages = sorted(messages, key=lambda x: x.time, reverse=True )

        # Query Lists:
        items = query_list.all()


        # add information for display in the webpage
        return render_template('trip_detail.html', username=username, name=name,
                    trip_name=trip_name, members=members, messages=sorted_messages,
                    trip_code=trip_code, items=items)
    else:
        flash("You are not logged in. Please do so.")
        return redirect('/')


@app.route('/message/<trip_code>', methods=["POST"])
def commit_message(trip_code):
    """Write messages to server """

    username = session['user']
    print trip_code

    message = request.form.get("mymessage")

    # Write message to database

    my_message = Comment(trip_code=trip_code, user_id=username, comment=message,
                         time=datetime.datetime.now())
    db.session.add(my_message)
    db.session.commit()
    return redirect("/trip_detail/"+trip_code)

@app.route('/list/<trip_code>', methods=["POST"])
def add_to_list(trip_code):
    """Adds items to list table"""

    #print trip_code

    username = session['user']
    list_item = request.form.get("description")
    print list_item
    user_id = request.form.get("userid")
    completed = request.form.get("completed")
    if not completed:
        completed = False


    # Write list to database

    my_list = List(trip_code=trip_code, user_id=user_id, description=list_item,
                        completed=completed)

    db.session.add(my_list)
    db.session.commit()
    return redirect("/trip_detail/"+trip_code)


@app.route('/add_member/<trip_code>', methods=["GET"])
def add_members_form(trip_code):
    """Option to add members to trip"""

    username = session['user']
    users = User.query.filter(User.user_id != username).all()

    return render_template("add_member.html", users=users, trip_code=trip_code)


@app.route('/add_member/<trip_code>', methods=["POST"])
def add_members(trip_code):
    """Add members to trip """

    users = User.query.all()

    pass


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
            db.session.delete(trip)

    else:
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

    
    app.run(port=5000, host='0.0.0.0')

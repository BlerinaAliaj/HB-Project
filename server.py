"""Hiker App"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Trip, UserTrip, Comment, List, Geodata, GeodataTrip, connect_to_db, db


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
            return redirect("/")
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

    else:
        flash("""That username is already taken. Please choose another one or
            go to login page""")
        return redirect("/register")

    return redirect('/')
    # return redirect('/profile')


# @app.route('/users')
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template("user_list.html", users=users)


# @app.route('/user_detail/<user_id>')
# def user_detail(user_id):
#     """User detail page"""

#     query_user = User.query.filter_by(user_id=user_id).first()

#     age = query_user.age
#     zipcode = query_user.zipcode
#     ratings = query_user.ratings

#     return render_template("user_detail.html", user_id=user_id, age=age, zipcode=zipcode, ratings=ratings)


# @app.route('/logout')
# def logout():
#     """Logs out user"""

#     del session["user"]
#     flash("You have been successfully logged out.")

#     return redirect('/')


# @app.route('/movies')
# def movie_list():
#     """Lists of movies"""

#     movies = Movie.query.order_by(Movie.title)

#     return render_template("movie_list.html", movies=movies)


# @app.route('/movie_detail/<movie_id>')
# def movie_detail(movie_id):
#     """User detail page"""

#     query_movie = Movie.query.filter_by(movie_id=movie_id).first()
#     title = query_movie.title
#     ratings = query_movie.ratings

#     if 'user' in session:
#         user_id = session['user']
#         user_rating = Rating.query.filter( (Rating.movie_id == movie_id) & (Rating.user_id == user_id) ).first()

#     return render_template("movie_detail.html", title=title, ratings=ratings, user_rating=user_rating, movie_id=movie_id)


# @app.route('/rate_movie', methods=["POST"])
# def rate_movie():

#     my_rating = request.form.get("my_rating")
#     movie_id = request.form.get("movie_id")
#     user_id = session['user']

#     query_rating = Rating.query.filter((Rating.user_id == user_id) & (Rating.movie_id == movie_id)).first()

#     if query_rating:
#         query_rating.score = my_rating

#     else:
#         new_rating = Rating(movie_id=movie_id,
#                         user_id=user_id,
#                         score=my_rating)
#         db.session.add(new_rating)

#     db.session.commit()
#     # else update the user/movie rating

#     return my_rating




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    app.run(port=5000, host='0.0.0.0')
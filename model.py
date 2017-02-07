"""Models and database functions for Hiker project."""

from flask_sqlalchemy import SQLAlchemy
import datetime
import correlation


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of of Hiker website
    User will create its own profile with 
    user name, 
    first name, 
    last name,
    email, 
    password,
    zipcode
    """

    __tablename__ = "users"

    user_id = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.String(15), nullable=True)


    def __repr__(self):
        """ Provide helpful representation when printed."""

        return "<User user_id=%s first_name=%s last_name=%s email=%s>" % (self.user_id,
            self.first_name, self.last_name, self.email)


class Trip(db.Model):
    """Trips table for all trips"""

    __tablename__ = "trips"

    trip_code = db.Column(db.String(10), primary_key=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_start = db.Column(db.DateTime, nullable=True)
    start_loc = db.Column(db.Integer, nullable=True)
    end_loc = db.Column(db.Integer, nullable=True)
    num_days = db.Column(db.Integer, nullable=True)



    def __repr__(self):
        """ Provide helpful representation when printed."""

        return "<Movie movie_id=%s title=%s>" % (self.movie_id, self.title)


class Rating(db.Model):
    """Rating of movies."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>"
        return s % (self.rating_id, self.movie_id, self.user_id,
                    self.score)


    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings",
                                               order_by=rating_id))


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
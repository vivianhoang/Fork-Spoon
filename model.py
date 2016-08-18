"""Models and database functions for food matching project."""

from flask_sqlalchemy import SQLAlchemy

# Connecting to the PostgreSQL database through the FLASK-SQLAlchemy helper library

db = SQLAlchemy()


# db.Model is the baseclass for all models.
class User(db.Model):
    """User of the food website."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)

    # make buttons to log in as user A or user B on homepage
    # location 127.0.0.1 /login/1 , and do for login 2

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User id=%s name=%s email=%s>" % (self.id,
                                                  self.first_name,
                                                  self.last_name,
                                                  self.email,
                                                  self.password)


class Event(db.Model):
    """User is creating a meal event"""

    __tablename__ = "events"

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    business_id = db.Column(db.Integer, db.ForeignKey("businesses.id"))
    is_matched = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    business = db.relationship("Business", backref=db.backref("events", order_by=id))

    category = db.relationship("Category", backref=db.backref("events", order_by=id))

    user = db.relationship("User", backref=db.backref("events", order_by=id))

    # backref is a simple way to also declare a new property on the Event class. You can then also use my_event.person (my_event is a pre-created query) to get to the person at that event.

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event id=%s start_time=%s end_time=%s category_id=%s business_id=%s is_matched=%s user_id=%s>" % (self.id,
                                                                                                                   self.start_time,
                                                                                                                   self.end_time,
                                                                                                                   self.category_id,
                                                                                                                   self.business_id,
                                                                                                                   self.is_matched,
                                                                                                                   self.user_id)


class Attendee(db.Model):
    """Users that are matched and attending the event."""

    __tablename__ = "attendees"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    is_owner = db.Column(db.Boolean, default=True)

    user = db.relationship("User",backref=db.backref("attendees", order_by=id))

    event = db.relationship("Event", backref=db.backref("attendees", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event id=%s user_id=%s event_id=%s is_owner=%s>" % (self.id,
                                                                     self.user_id,
                                                                     self.event_id,
                                                                     self.is_owner)


class Business(db.Model):
    """Individual Business Information."""

    __tablename__ = "businesses"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review_count = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event id=%s name=%s location=%s rating=%s review_count=%s url=%s>" % (self.id,
                                                                                       self.name,
                                                                                       self.location,
                                                                                       self.rating,
                                                                                       self.review_count,
                                                                                       self.url)


class Category(db.Model):
    """Types of food users can search for."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food_type = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event id=%s food_type=%s>" % (self.id,
                                               self.food_type)


class City(db.Model):
    """City locations user can search for."""

    __tablename__ = "cities"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Event id=%s city=%s>" % (self.id,
                                          self.city_name)

################################################################################


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # created.db 'food' in virtual env, ran model.py, then created all in my model, then run seed to populate table.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///food'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

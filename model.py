"""Models and database functions for food matching project."""

from flask_sqlalchemy import SQLAlchemy

# Connecting to the PostgreSQL database through the FLASK-SQLAlchemy helper library

db = SQLAlchemy()


# db.Model is the baseclass for all models.
class User(db.Model):
    """User of the food website."""

    __tablename__ = "users"

    # id is not used
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("phone_num.id"))
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    phone = db.relationship("Phone", backref=db.backref("users", order_by=id))

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User id=%s user_id=%s first_name=%s last_name=%s email=%s password=%s description=%s> " % (self.id,
                               self.user_id,
                               self.first_name,
                               self.last_name,
                               self.email,
                               self.password,
                               self.description)


class Phone(db.Model):
    """User's verified phone number."""

    __tablename__ = "phone_num"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    phone = db.Column(db.String(10), nullable=True, unique=True)
    code = db.Column(db.String(4), nullable=True)

    user = db.relationship("User", backref=db.backref("phone_num", order_by=id))

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Phone id=%s phone=%s code=%s>" % (self.id,
                                                  self.phone,
                                                  self.code)


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
    user_id = db.Column(db.Integer, db.ForeignKey("phone_num.id"))

    business = db.relationship("Business", backref=db.backref("events", order_by=id))

    category = db.relationship("Category", backref=db.backref("events", order_by=id))

    phone = db.relationship("Phone", backref=db.backref("events", order_by=id))

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
    user_id = db.Column(db.Integer, db.ForeignKey("phone_num.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    is_owner = db.Column(db.Boolean, default=True)

    phone = db.relationship("Phone", backref=db.backref("attendees", order_by=id))

    event = db.relationship("Event", backref=db.backref("attendees", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Attendee id=%s user_id=%s event_id=%s is_owner=%s>" % (self.id,
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
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Business id=%s name=%s location=%s rating=%s review_count=%s url=%s lat=%s lon=%s>" % (self.id,
                                                                                                        self.name,
                                                                                                        self.location,
                                                                                                        self.rating,
                                                                                                        self.review_count,
                                                                                                        self.url,
                                                                                                        self.lat,
                                                                                                        self.lng)


class Category(db.Model):
    """Types of food users can search for."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food_type = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category id=%s food_type=%s>" % (self.id,
                                                  self.food_type)


class City(db.Model):
    """City locations user can search for."""

    __tablename__ = "cities"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<City id=%s city=%s>" % (self.id,
                                         self.city_name)


def example_data():
    user = User(id=1, user_id=1234, first_name="Gordon", last_name="Ramsay", email="gramsay@gmail.com", password="123")
    user2 = User(id=2, user_id=4321, first_name="Joe", last_name="B", email="j@gmail.com", password="123")
    user3 = User(id=3, user_id=9876, first_name="Katie", last_name="Pep", email="kpep@gmail.com", password="123")
    phone = Phone(id=1234, phone="1234567890", code="1234")
    phone2 = Phone(id=4321, phone="0987654321", code="5678")
    phone3 = Phone(id=9876, code="2468")
    business = Business(name="Good Eats", location="123 Nowhere St., FakeCity, FakeState FakeZipcode", rating=4.5, review_count=1010, url="http://www.afakeurllink.com", lat=-25, lng=131)
    category = Category(food_type="American")
    event = Event(start_time="01/01/2016 01:00", end_time="01/01/2016 02:00", category_id=1, business_id=1, is_matched=False, user_id=1234)
    attendee = Attendee(user_id=1234, event_id=1, is_owner=True)
    attendee = Attendee(user_id=4321, event_id=1, is_owner=False)
    city = City(city_name="Paris")

    db.session.add_all([user, user2, user3, phone, phone2, phone3, event, attendee, business, category, city])
    db.session.commit()
################################################################################


def connect_to_db(app, db_uri='postgresql:///food'):
    """Connect the database to our Flask app."""

    # created.db 'food' in virtual env, ran model.py, then created all in my model, then run seed to populate table.
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

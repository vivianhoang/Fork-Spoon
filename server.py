"""Anonymous Eats"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
#from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from model import connect_to_db, db, User, Event, Attendee, Business, Category, City
from pytz import timezone
import os

auth = Oauth1Authenticator(

    consumer_key=os.environ['consumer_key'],
    consumer_secret=os.environ['consumer_secret'],
    token=os.environ['token'],
    token_secret=os.environ['token_secret']
)

client = Client(auth)

app = Flask(__name__)
app.secret_key = "ABC"  # change this

# Used so that if there is an error with our Jinja variables that we've made, it will raise an error
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Welcome Page."""

    return render_template('welcomepage.html')


@app.route('/login', methods=["GET"])
def login_page():
    """Shows login page."""

    return render_template('login.html')


@app.route('/signup')
def signup_page():
    """Show sign up page"""

    return render_template('signup.html')


@app.route('/login', methods=["POST"])
def login_processed():
    """Processes old users."""

    # checking to see if the user exists through email. If so, set a session cookie.
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Oops, you don't exist yet! Please sign up.")
        return redirect('/signup')
    if user.password != password:
        flash("The password you have given is incorrect.")
        return redirect('/login')

    session['id'] = user.id

    flash("Welcome back, %s. You have successfully logged in." % user.first_name)
    return redirect("/")


@app.route('/signup', methods=['POST'])
def signup_processed():
    """Processes new users."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    zipcode = request.form["zipcode"]
    password = request.form["password"]

    # checking to see if the email already exists in the db. If not, a new account is created.
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Oops, your email already exists! Please log in.")
        return redirect("/login")
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        zipcode=zipcode,
                        password=password)

    db.session.add(new_user)
    db.session.commit()

    session['id'] = new_user.id
    user = User.query.filter_by(email=email).first()

    flash("Welcome to Food Adventures, %s. You have successfully logged in." % user.first_name)
    return redirect("/")


@app.route("/logout")
def logout():
    """Logs user out"""

    # Log out and remove session cookie.
    session.clear()

    flash("You have successfully logged out.")
    return redirect("/")


@app.route("/profile/<int:id>", methods=['GET'])
def profile(id):
    """Displays user's profile"""

    user = User.query.get(id)
    return render_template("profile.html", user=user)


@app.route("/create_event")
def event_page():
    """Displays event creation page and forms to query through Yelp restaurants."""

    categories = Category.query.all()
    cities = City.query.all()

    return render_template("event.html", categories=categories, cities=cities)


@app.route("/restaurant_query", methods=['POST'])
def restaurants():
    """Displays restaurants to choose from."""

    city = request.form['city']
    zipcode = request.form['zipcode']
    term = request.form['term']
    radius_filter = request.form['distance']

    # taking into account both city and zipcode from search
    location = (city + " " + zipcode)

    params = {
        'term': term,
        'radius_filter': radius_filter,
        'sort': 0
    }

    results = client.search(location, **params)

    businesses = results.businesses
    category = Category.query.filter_by(food_type=term).first()
    category_id = category.id

    times = ["00:00", "00:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30",
             "5:00", "5:30", "6:00", "6:30", "7:00", "7:30", "8:00", "8:30", "9:00", "9:30",
             "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00",
             "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30",
             "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"]

    return render_template("restaurants.html", businesses=businesses, times=times, category_id=category_id)


@app.route("/confirmation", methods=["POST"])
def event_confirmed():
    """Confirmation page after creating an event."""

    # instantiating event, business, and single attendees into our tables

    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    date_start_time = date + " " + start_time
    date_end_time = date + " " + end_time

    start_datetime = datetime.strptime(date_start_time, "%m/%d/%Y %H:%M")
    end_datetime = datetime.strptime(date_end_time, "%m/%d/%Y %H:%M")

    # convert time to local UTC

    business_name = request.form['business_name']
    business_address = request.form['business_location']
    business_rating = request.form['business_rating']
    business_review_count = request.form['business_review_count']
    business_url = request.form['business_url']

    business = Business.query.filter_by(url=business_url).first()

    # checking to see if business is not there and instantiating a new business
    # If the business is already in DB we only instantiate the event

    if not business:
        new_business = Business(name=business_name, location=business_address, rating=business_rating, review_count=business_review_count, url=business_url)

        db.session.add(new_business)
        db.session.commit()

    # getting category id and business id to pass into event
    category_id = request.form['category_id']
    business = Business.query.filter_by(name=business_name).first()
    business_id = business.id

    user = User.query.filter_by(id=session['id']).first()
    event = Event(start_time=start_datetime, end_time=end_datetime, category_id=category_id, business_id=business_id, user_id=user.id)

    db.session.add(event)
    db.session.commit()

    event = Event.query.filter_by(business_id=business_id).first()
    event_id = event.id

    # instantiating the attendee page so that it shows the creater is the owner/is attending. If there is a match, we can query through it and two rows will show up via event_id. If not, only one attendee will appear.
    attendee = Attendee(user_id=user.id, event_id=event_id, is_owner=True)

    db.session.add(attendee)
    db.session.commit()

    return render_template("confirmation.html", event=event)


@app.route("/upcoming_events", methods=['GET'])
def upcomming_events():
    """Displays events user has created and matched with"""

    pacific = timezone('US/Pacific')
    time_now = datetime.now(tz=pacific)

    # looking for all unmatched events that haven't passed their date
    user = User.query.filter_by(id=session['id']).first()
    unmatched_events = Event.query.filter(Event.is_matched == False, Event.user_id == user.id, Event.end_time > time_now).all()  # Event.end_time > time_now

    # checking all events the user is planning to go to
    matched_event = Attendee.query.filter_by(user_id=user.id).all()

    # checking to see if the event is matched with someone else. If so, it is an UPCOMMING event
    my_matched_events = []
    for a in matched_event:
        if a.event.is_matched == True:
            my_matched_events.append(a)

    # grabs all previous events, both matched and unmatched
    previous_events = Event.query.filter(Event.user_id == user.id, Event.end_time < time_now).all()
    # previous_events = db.session.query(Attendee).join(Attendee.event).filter(Attendee.user_id == user.id, Event.end_time < time_now).all()

    # my_previous_events = []

    # for a in previous_events:
    #     if a.is_matched == True:
    #         my_previous_events.append(a)

    return render_template("upcoming_events.html", unmatched_events=unmatched_events, my_matched_events=my_matched_events, previous_events=previous_events, time_now=time_now)


@app.route("/find_events", methods=['GET'])
def available_events():
    """Displaying all events that are available, not including the current user's created events."""

    pacific = timezone('US/Pacific')
    time_now = datetime.now(tz=pacific)

    # DEAL WITH TIME
    user = User.query.filter_by(id=session['id']).first()
    events = Event.query.filter(Event.is_matched == False, Event.user_id != user.id, Event.end_time > time_now).all()
    # The past is less than the present/now, so we want to show all events where the future is greater than the present/now

    return render_template("available_events.html", events=events)


@app.route("/matched", methods=['POST'])
def matched_event():
    """Instantiating attendees after a user selects an event."""

    event_id = request.form['event_id']
    # updates is_matched to true so it won't show up on the /find_events page anymore.
    Event.query.filter_by(id=event_id).update({"is_matched": True})

    db.session.commit()

    user = User.query.filter_by(id=session['id']).first()

    # instantiating current user to attendees after selecting an event. Since the user is connecting to this particular event, they are not the owner, so is_owner is false.
    attendee = Attendee(user_id=user.id, event_id=event_id, is_owner=False)

    db.session.add(attendee)
    db.session.commit()

    flash("You have a new meal plan!")

    return redirect("/upcoming_events")


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    #DebugToolbarExtension(app)

    # Since we ran on vagrant, we need to put host equal to 0.0.0.0
    app.run(host="0.0.0.0")

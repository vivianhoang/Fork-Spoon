"""Anonymous Eats"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
#from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from google_key import GOOGLE_KEY
from twilio.rest import TwilioRestClient
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from model import connect_to_db, db, User, Event, Attendee, Business, Category, City, Phone
from db_func_test import get_specific_event, get_specific_attendee, get_specific_user, get_specific_business, update_phone
from pytz import timezone
import random
from flask import jsonify
import os
import oauth2

# Authenticating TWILIO
ACCOUNT_SID = os.environ['TWILIO_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_KEY']

twilio_client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# Authenticating YELP
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


def generate_verification_code():
    """Generates a random 4 digit code.

       >>> import random

       >>> random.seed(1)

       >>> generate_verification_code()
       '1762'

       >>> generate_verification_code()
       '4457'

       >>> generate_verification_code()
       '0073'

    """
    numbers = []

    for _ in range(4):
        numbers.append(str(random.randrange(9)))

    return "".join(numbers)


def generate_user_id():
    """Generates a random 9 digit user_id.

       >>> import random

       >>> random.seed(2)

       >>> generate_user_id()
       8007662

       >>> generate_user_id()
       5513

       >>> generate_user_id()
       688

    """
    numbers = []

    # need to fix so all id's will be unique
    for _ in range(random.randrange(8)):
        numbers.append(str(random.randrange(9)))

    joined_nums = "".join(numbers)
    return int(joined_nums)


def miles_to_meters(mile):
    """Converts miles input to meters.

       >>> miles_to_meters(5)
       8046.735439432223

       >>> miles_to_meters(1)
       1609.3470878864446

       >>> miles_to_meters(20)
       32186.94175772889

    """

    mile = float(mile)
    meter_conversion = 0.00062137
    meters = mile / meter_conversion

    return meters


def yelp_API_call(location, params):
    """Creates a call to Yelp's API and returns the results."""

    return client.search(location, **params)


@app.route('/')
def index():
    """Welcome Page."""

    return render_template('welcomepage.html')


@app.route('/login', methods=["GET"])
def login_page():
    """Shows login page."""

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_processed():
    """Processes old users."""

    # checking to see if the user exists through email. If so, set a session cookie.
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Oops, you don't exist yet! Please sign up.")
        return redirect('/enter_phone')
    if user.password != password:
        flash("The password you have given is incorrect.")
        return redirect('/login')

    session['id'] = user.user_id

    flash("Welcome back, %s. You have successfully logged in." % user.first_name)
    return redirect("/")


@app.route('/enter_phone')
def enter_phone():

    return render_template("enter_phone.html")


@app.route('/submit_phone', methods=["POST"])
def submit_phone():

    verification_code = generate_verification_code()
    phone_number = request.form["phone_number"]
    user_id = generate_user_id()

    find_phone = Phone.query.filter_by(phone=phone_number).first()

    if not find_phone:

        full_phone = '+1' + phone_number

        twilio_client.messages.create(
            to=full_phone,
            from_='+16506514651',
            body='Your verification code is ' + verification_code + ".",
        )

        new_phone = Phone(code=verification_code, id=user_id)

        db.session.add(new_phone)
        db.session.commit()
    else:
        flash("That number is already taken.")
        return redirect("/enter_phone")

    return render_template("verification.html", phone_number=phone_number, verification_code=verification_code, user_id=user_id)


@app.route('/submit_confirmation_code', methods=["POST"])
def verification():

    user_id = request.form['user_id']
    phone_number = request.form['phone_number']
    private_info = Phone.query.filter_by(id=user_id).first()
    phone_verification_code = private_info.code

    submitted_verification_code = request.form["verification_code"]

    if phone_verification_code == submitted_verification_code:
        # go to sign up page
        return render_template("signup.html", user_id=user_id, phone_number=phone_number)
    else:
        flash("Invalid code.")
        return render_template("verification.html", user_id=user_id, phone_number=phone_number)


@app.route('/signup', methods=['POST'])
def signup_processed():
    """Processes new users."""

    user_id = request.form["user_id"]
    phone_number = request.form["phone_number"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]

    # checking to see if the email already exists in the db. If not, a new account is created.
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Oops, your email already exists! Please log in.")
        return redirect("/login")
    else:
        new_user = User(user_id=user_id,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password)

        # used in test to update phone number
        update_phone(user_id, phone_number)

    #when I instantiatiate the ID, I need to refer to the id from the phone number table

    db.session.add(new_user)
    db.session.commit()

    session['id'] = new_user.user_id
    user = get_specific_user(email)

    flash("Welcome to Food Adventures, %s. You have successfully logged in." % user.first_name)
    return render_template("welcomepage.html")


@app.route("/logout")
def logout():
    """Logs user out"""

    # Log out and remove session cookie.
    session.clear()

    flash("You have successfully logged out.")
    return redirect("/")


@app.route("/profile/<int:id>")
def profile(id):
    """Displays/saves user's profile"""

    user = User.query.filter_by(user_id=session['id']).first()

    return render_template("profile.html", user=user)


@app.route("/profile-edit", methods=['POST'])
def edit_profile():
    """Displays/saves user's profile"""

    description = request.form.get("description")
    User.query.filter_by(user_id=session['id']).update({"description": description})

    db.session.commit()

    return "You have successfully updated your profile."


@app.route("/create_event")
def make_search():
    """Displays event creation page and forms to query through Yelp restaurants."""

    categories = Category.query.all()
    cities = City.query.all()

    return render_template("event.html", categories=categories, cities=cities)


@app.route("/restaurant_query", methods=['POST'])
def complete_event():
    """Displays restaurants to choose from."""

    city = request.form['city']
    zipcode = request.form['zipcode']
    term = request.form['term']
    radius_filter = request.form['distance']

    location = (city + " " + zipcode)

    params = {
        'term': term,
        'radius_filter': miles_to_meters(radius_filter),
        'sort': 0
    }

    results = yelp_API_call(location, params)  # LIVE YELP CALL

    # instantiating new businesses that we find.
    businesses = results.businesses
    category = Category.query.filter_by(food_type=term).first()
    category_id = category.id

    for business in businesses:
        find_business = Business.query.filter_by(url=business.url, name=business.name).first()
        if not find_business:
            new_business = Business(name=business.name, location=', '.join(business.location.display_address), rating=business.rating, review_count=business.review_count, url=business.url, lat=business.location.coordinate.latitude, lng=business.location.coordinate.longitude)
            db.session.add(new_business)
            db.session.commit()

    times = ["00:00", "00:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30",
             "5:00", "5:30", "6:00", "6:30", "7:00", "7:30", "8:00", "8:30", "9:00", "9:30",
             "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00",
             "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30",
             "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"]

    ##########################
    # Cannot jsonify in a separate route, so preparing for immediate use

    business_name = []
    business_lat = []
    business_lng = []
    business_rating = []
    business_reviews = []
    business_url = []
    business_address = []

    for business in businesses:
        business_name.append(business.name)
        business_lat.append(business.location.coordinate.latitude)
        business_lng.append(business.location.coordinate.longitude)
        business_rating.append(business.rating)
        business_reviews.append(business.review_count)
        business_url.append(business.url)
        business_address.append(', '.join(business.location.display_address))

    return render_template("restaurants.html", GOOGLE_KEY=GOOGLE_KEY, businesses=businesses, times=times, category_id=category_id, business_name=business_name, business_lat=business_lat, business_lng=business_lng, business_rating=business_rating, business_url=business_url, business_reviews=business_reviews, business_address=business_address)


@app.route("/confirmation", methods=["POST"])
def event_confirmed():
    """Confirmation page after creating an event."""

    # instantiating event and single attendees into our tables

    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    date_start_time = date + " " + start_time
    date_end_time = date + " " + end_time

    start_datetime = datetime.strptime(date_start_time, "%m/%d/%Y %H:%M")
    end_datetime = datetime.strptime(date_end_time, "%m/%d/%Y %H:%M")

    business_url = request.form['business_url']
    business = get_specific_business(business_url)

    # getting category id and business id to instantiate event
    category_id = request.form['category_id']
    business_id = business.id

    user = User.query.filter_by(user_id=session['id']).first()
    event = Event(start_time=start_datetime, end_time=end_datetime, category_id=category_id, business_id=business_id, user_id=user.user_id)

    db.session.add(event)
    db.session.commit()

    event = get_specific_event(business_id)
    event_id = event.id

    # instantiating the attendee page so that it shows the creater is the owner/is attending. If there is a match, we can query through it and two rows will show up via event_id. If not, only one attendee will appear.
    attendee = Attendee(user_id=user.user_id, event_id=event_id, is_owner=True)

    db.session.add(attendee)
    db.session.commit()

    return render_template("confirmation.html", event=event)


@app.route("/upcoming_events", methods=['GET'])
def upcomming_events():
    """Displays events user has matched with and/or created"""

    pacific = timezone('US/Pacific')
    time_now = datetime.now(tz=pacific)

    # looking for all unmatched events that haven't passed their date
    user = User.query.filter_by(user_id=session['id']).first()
    unmatched_events = Event.query.filter(Event.is_matched == False, Event.user_id == user.user_id, Event.end_time > time_now).all()

    # query through attendees to get all events of the current user
    matched_event = get_specific_attendee(user.user_id)

    # Grabbing all my matched events. Preparing to look for other match.
    # this can be written better
    my_matched_events = []
    for a in matched_event:
        if a.event.is_matched == True:
            my_matched_events.append(a)

    # grabbing the matched event_id.
    same_event_id = []
    for a in my_matched_events:
        same_event_id.append(a.event_id)

    # filtering the events where the attendee has the same event_id but making sure that the current user's name doesn't show up when we include a link to their profile page. Used to display the event info and link to other_person's profile page.
    other_person_that_matched_with_user = []
    for event_id in same_event_id:
        other_person = Attendee.query.filter(Attendee.user_id != user.user_id, Attendee.event_id == event_id).first()
        other_person_that_matched_with_user.append(other_person)

    # grabs all previous events, both matched and unmatched
    previous_events = Event.query.filter(Event.user_id == user.user_id, Event.end_time < time_now).all()

    return render_template("upcoming_events.html", unmatched_events=unmatched_events, other_persons=other_person_that_matched_with_user, previous_events=previous_events, time_now=time_now)


@app.route("/find_events", methods=['GET'])
def available_events():
    """Displaying all events that are available, not including the current user's created events."""

    pacific = timezone('US/Pacific')
    time_now = datetime.now(tz=pacific)

    user = User.query.filter_by(user_id=session['id']).first()

    # The past is less than the present/now, so we want to show all events where the future is greater than the present/now
    events = Event.query.filter(Event.is_matched == False, Event.user_id != user.user_id, Event.end_time > time_now).all()

    return render_template("find_events.html", events=events)


@app.route("/matched", methods=['POST'])
def matched_event():
    """Instantiating attendees after a user selects an event and matches with someone."""

    event_id = request.form['event_id']
    Event.query.filter_by(id=event_id).update({"is_matched": True})

    db.session.commit()

    user = User.query.filter_by(user_id=session['id']).first()

    # instantiating current user to attendees after selecting an event. Since the user is connecting to this particular event, they are not the owner, so is_owner is false.
    attendee = Attendee(user_id=user.user_id, event_id=event_id, is_owner=False)

    db.session.add(attendee)
    db.session.commit()

    flash("You have a new meal plan!")

    return redirect("/upcoming_events")


@app.route("/other_profile/<int:id>", methods=['GET'])
def other_profile(id):
    """Displays other user's profile"""

    # need to figure out how to display anyone's page if I look for specific ID

    user = User.query.filter_by(user_id=id).first()
    return render_template("other_user_profile.html", user=user)


if __name__ == "__main__":
    from doctest import testmod
    if testmod().failed == 0:
        app.debug = True

        connect_to_db(app)

        #DebugToolbarExtension(app)

        # Since we run on vagrant, we need to put host equal to 0.0.0.0
        app.run(host="0.0.0.0")

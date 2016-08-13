"""Connecting Solo Eaters"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
#from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from model import connect_to_db, db, User, Event, Attendee, Business, Category
import os

auth = Oauth1Authenticator(

    consumer_key=os.environ['consumer_key'],
    consumer_secret=os.environ['consumer_secret'],
    token=os.environ['token'],
    token_secret=os.environ['token_secret']
)

# auth = Oauth1Authenticator(**{
#     "consumer_key": "",
#     "consumer_secret": "",
#     "token": "",
#     "token_secret": ""
# })

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

    # rendering login page
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    """Show sign up page"""
    # rendering signup page

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
    return redirect("/")  # redirect elsewhere later (maybe profile)


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
                        # yelp_token="",
                        # yelp_token_secret="")

    db.session.add(new_user)

    db.session.commit()

    session['id'] = new_user.id

    user = User.query.filter_by(email=email).first()

    flash("Welcome to Food Adventures, %s. You have successfully logged in." % user.first_name)
    return redirect("/")  # redirect elsewhere later (maybe profile)


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


@app.route("/upcoming_events", methods=['GET'])
def upcomming_events():
    """Displays events user has created and matched with"""

    return render_template("event_detail.html")


@app.route("/create_event")
def event_page():
    """Displays event creation page and forms to query through Yelp restaurants."""

    categories = Category.query.all()

    return render_template("event.html", categories=categories)


@app.route("/restaurant_query", methods=['POST'])
def restaurants():
    """Displays restaurants to choose from."""

    city = request.form['city']  # this is the same
    zipcode = request.form['zipcode']  # as this
    term = request.form['term']
    radius_filter = request.form['distance']

    location = (city + " " + zipcode)

    params = {
        'term': term,
        'radius_filter': radius_filter,
        'sort': 0
    }

    results = client.search(location, **params)

    businesses = results.businesses

    times = ["00:00", "00:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30",
             "5:00", "5:30", "6:00", "6:30", "7:00", "7:30", "8:00", "8:30", "9:00", "9:30",
             "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00",
             "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18.30",
             "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00", "22:30", "23:00", "23:30"]

    return render_template("restaurants.html", businesses=businesses, times=times)


@app.route("/confirmation", methods=["POST"])
def event_confirmed():
    """Confirmation page after creating an event."""

    date = request.form('date')
    start_time = request.form('start_time')
    end_time = request.form('end_time')

    start_datetime = datetime.strptime(date, start_time, "%d-%b-%Y")
    end_datetime = datetime.striptime(date, end_time, "%d-%b-%Y")

    business_name = request.form('business_name')
    business_address = request.form('business_address')
    business_rating = request.form('business_rating')
    business_review_count = request.form('business_review_count')
    business_url = request.form('business_url')
    #instantiate event and business

    event = Event()
    business = Business()

    db.session.add_all(event, business)  # add all

    db.session.commit()

    return render_template("confirmation.html")


if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    #DebugToolbarExtension(app)

    # Since we ran on vagrant, we need to put host equal to 0.0.0.0
    app.run(host="0.0.0.0")

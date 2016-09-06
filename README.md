Fork&Spoon
--------

**Description**

Fork&Spoon gives single eaters the exciting option to anonymously invite one other eater to join them on their dining festivities within the San Francisco Bay Area. 

**How It Works**

Fork&Spoon uses Google Maps and Yelp so users can quickly find and select nearby places while choosing a date and time that suits them best. Other single eaters can choose from a list of available outings; when they choose an outing, a text message is sent via Twilio. Voilà! A meal date for two has been made! Users now have the chance to meet and eat with new individuals while exploring the places they've always wanted to try. 

### Technology Stack

**Application:** Python, Flask, Jinja, SQLAlchemy, PostgreSQL, JavaScript

**APIs:** Yelp, Google Map, Twilio 

**Front-End**: HTML/CSS, Bootstrap, JQuery, AJAX    


### Screenshots

**Searching For Businesses (User 1)**

<img src="/static/css/search_businesses.png">

**Search Results**

<img src="/static/css/search_results.png">

**Finding Events to Join (User 2)**

<img src="/static/css/find_events.png">

**Viewing New, Upcoming, and Previous Events**

<img src="/static/css/your_events.png">



### Testing Coverage

**Types of Tests: **Doctests, Unittests, Integration Testing of Flask

<img src="/static/css/coverage.png" height="350">


### Running Fork&Spoon Locally

Clone this repository:

```
> git clone https://github.com/vivianhoang/Fork-Spoon.git
```


Create a virtual environment: 

```
> virtualenv env
> source env/bin/activate
```

Install the dependencies:

```
> pip install -r requirements.txt
```

Get an API key from Yelp, Google Maps, and Twilio, and store in a secrets.sh. Put the file in your .gitignore.

Run PostgreSQL and create a database named forkspoon:

```
> createdb forkspoon
```

Run model.py interactively and create your psql tables:

```
> python -i model.py
Connected to DB.
>>> db.create_all()
```

Seed the database with cities and search terms:

```
> python seed.py
```

To run the app, start the server:

```
> python server.py
```

In your browswer, go to lcalhost:5000/ to start using Fork&Spoon!


### About the Developer    
Vivian Tse Hoang is a software engineer currently residing in the San Francisco Bay Area.

[Email](mailto:viviantsehoang@gmail.com) | [Linkedin](https://www.linkedin.com/in/vivhoang) | [Twitter](http://twitter.com/imvivianhoang)        
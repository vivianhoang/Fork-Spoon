import unittest
from unittest import TestCase
from server import app
from model import db, example_data, connect_to_db
from db_func_test import get_specific_event, get_specific_attendee, get_specific_user


class FlaskTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Food Adventures", result.data)

    def test_logout(self):
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("You have successfully logged out", result.data)


class FlaskDatabaseTests(TestCase):

    def setUp(self):
        """Flask tests that use the database.."""

        # gets the Flask test client
        self.client = app.test_client()

        # show Flask errors that happen during the tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['id'] = 1

        # connect to test database
        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

    def tearDown(self):
        """Stuff to do after each test."""

        db.session.close()
        db.drop_all()

    def test_signup_fail(self):
        result = self.client.post("/signup",
                                  data={"first_name": "Gordon",
                                        "last_name": "Ramsay",
                                        "email": "gramsay@gmail.com",
                                        "password": "123"},
                                  follow_redirects=True)
        self.assertIn("Oops, your email already exists", result.data)

    # def tests_signin(self):
    #     result = self.client.post("/signup",
    #                               data={"id": 2,
    #                                     "first_name": "Horrible",
    #                                     "last_name": "Name",
    #                                     "email": "hname@gmail.com",
    #                                     "password": "456"},
    #                               follow_redirects=True)
    #     self.assertIn("Welcome to Food Adventures, Horrible", result.data)

    def test_user(self):
        result = self.client.post("/login",
                                  data={"email": "gramsay@gmail.com",
                                        "password": "123"},
                                  follow_redirects=True)
        self.assertIn("Welcome back,", result.data)

    def test_get_user(self):
        email = "gramsay@gmail.com"

        user = get_specific_user(email)
        self.assertEqual(user.first_name, "Gordon")

    def test_get_event(self):
        business_id = 1

        event = get_specific_event(business_id)
        self.assertEqual(event.id, 1)

    def test_get_attendee(self):
        user_id = 1

        attendee = get_specific_attendee(user_id)
        self.assertEqual(attendee[0].is_owner, True)

    def test_categories(self):
        result = self.client.get("/create_event",
                                 data={"categories": "American"},
                                 follow_redirects=True)

        self.assertIn("American", result.data)

    def test_cities(self):
        result = self.client.get("/create_event",
                                 data={"cities": "Paris"},
                                 follow_redirects=True)

        self.assertIn("Paris", result.data)

    def test_profile(self):
        result = self.client.get("profile/1", follow_redirects=True)

        self.assertIn("<p>USER\'S PROFILE!</p>", result.data)

        ##### TEST CITY, CATEGORY, BUSINESS

    # def test_restaurant_query(self):
    #     result = self.client.post("/restaurant_query",
    #                               data={"city": "Paris",
    #                                     "zipcode": "",
    #                                     "term": "American",
    #                                     "radius_filter": 3},
    #                               follow_redirects=True)

    #     self.assertIn("<h6>*Don't forget to check business hours before hand!</h6>", result.data)

    # def test_confirmation(self):
    #     result = self.client.post("/confirmation",
    #                               data={"date": "01/01/2016",
    #                                     "start_time": "01:00",
    #                                     "end_time": "02:00"},
    #                               follow_redirects=True)  # how to check a POST with relationship walking?

    #     self.assertIn("Thanks for creating an event", result.data)

    def test_find_events(self):
        result = self.client.get("/find_events")

        self.assertIn("<p>Oops! There are currently no events available :\'(</p>", result.data)

    def test_matched(self):
        result = self.client.post("/matched",
                                  data={"event_id": "1"},
                                  follow_redirects=True)

        self.assertIn("You have a new meal plan!", result.data)

    def test_upcoming_events(self):
        result = self.client.get("/upcoming_events")

        self.assertIn("<p>You have no upcoming matched events :( </p>", result.data)


if __name__ == "__main__":
    unittest.main()

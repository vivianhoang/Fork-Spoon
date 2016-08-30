import unittest
from unittest import TestCase
from server import app
from model import db, example_data, connect_to_db
from db_func_test import get_specific_event, get_specific_attendee, get_specific_user, get_specific_business, _mock_yelp_API_call
import server


class FlaskTests(TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1234

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
        self.client = server.app.test_client()

        # show Flask errors that happen during the tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['id'] = 1234

        # connect to test database
        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

        def _mock_yelp_API_call(location, params):

            results = {
                        "region": {
                            "span": {
                                "latitude_delta": 0.0,
                                "longitude_delta": 0.0
                            },
                            "center": {
                                "latitude": 48.856614,
                                "longitude": 2.3522219
                            }
                        },
                        "total": 3,
                        "businesses": [
                            {
                                "is_claimed": False,
                                "rating": 2.5,
                                "mobile_url": "http://m.yelp.com/biz/quick-paris-20?adjust_creative=DhkXE_EgW2WTJ7X-20so4Q&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=DhkXE_EgW2WTJ7X-20so4Q",
                                "rating_img_url": "https://s3-media4.fl.yelpcdn.com/assets/2/www/img/c7fb9aff59f9/ico/stars/v1/stars_2_half.png",
                                "review_count": 6,
                                "name": "Quick",
                                "rating_img_url_small": "https://s3-media4.fl.yelpcdn.com/assets/2/www/img/8e8633e5f8f0/ico/stars/v1/stars_small_2_half.png",
                                "url": "http://www.yelp.com/biz/quick-paris-20?adjust_creative=DhkXE_EgW2WTJ7X-20so4Q&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=DhkXE_EgW2WTJ7X-20so4Q",
                                "categories": [
                                    [
                                        "Fast Food",
                                        "hotdogs"
                                    ],
                                    [
                                        "American (Traditional)",
                                        "tradamerican"
                                    ]
                                ],
                                "phone": "+33147737654",
                                "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/hP_yeWopMWGBcIuAXfWFAg/ms.jpg",
                                "location": {
                                    "city": "Paris",
                                    "display_address": [
                                        "2 Le Parvis de la Défense",
                                        "Centre Commercial les 4 temps",
                                        "4ème",
                                        "92800 Paris",
                                        "France"
                                    ],
                                    "geo_accuracy": 9.5,
                                    "neighborhoods": [
                                        "4ème",
                                        "Marais"
                                    ],
                                    "postal_code": "92800",
                                    "country_code": "FR",
                                    "address": [
                                        "2 Le Parvis de la Défense",
                                        "Centre Commercial les 4 temps"
                                    ],
                                    "coordinate": {
                                        "latitude": 48.856614,
                                        "longitude": 2.3522219
                                    },
                                    "state_code": "75"
                                },
                                "display_phone": "+33 1 47 73 76 54",
                                "rating_img_url_large": "https://s3-media2.fl.yelpcdn.com/assets/2/www/img/d63e3add9901/ico/stars/v1/stars_large_2_half.png",
                                "id": "quick-paris-20",
                                "is_closed": False
                            },
                            {
                                "is_claimed": False,
                                "rating": 2.5,
                                "mobile_url": "http://m.yelp.com/biz/mac-donalds-paris-4?adjust_creative=DhkXE_EgW2WTJ7X-20so4Q&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=DhkXE_EgW2WTJ7X-20so4Q",
                                "rating_img_url": "https://s3-media4.fl.yelpcdn.com/assets/2/www/img/c7fb9aff59f9/ico/stars/v1/stars_2_half.png",
                                "review_count": 3,
                                "name": "Mac donald's",
                                "rating_img_url_small": "https://s3-media4.fl.yelpcdn.com/assets/2/www/img/8e8633e5f8f0/ico/stars/v1/stars_small_2_half.png",
                                "url": "http://www.yelp.com/biz/mac-donalds-paris-4?adjust_creative=DhkXE_EgW2WTJ7X-20so4Q&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=DhkXE_EgW2WTJ7X-20so4Q",
                                "categories": [
                                    [
                                        "American (Traditional)",
                                        "tradamerican"
                                    ]
                                ],
                                "phone": "+33147730853",
                                "image_url": "https://s3-media1.fl.yelpcdn.com/bphoto/KXcCa8a-aA-qsaOPfjFCyg/ms.jpg",
                                "location": {
                                    "city": "Paris",
                                    "display_address": [
                                        "Centre Commercial les 4 temps",
                                        "4ème",
                                        "Paris",
                                        "France"
                                    ],
                                    "geo_accuracy": 9.5,
                                    "neighborhoods": [
                                        "4ème",
                                        "Marais"
                                    ],
                                    "country_code": "FR",
                                    "address": [
                                        "Centre Commercial les 4 temps"
                                    ],
                                    "coordinate": {
                                        "latitude": 48.856614,
                                        "longitude": 2.3522219
                                    },
                                    "state_code": "75"
                                },
                                "display_phone": "+33 1 47 73 08 53",
                                "rating_img_url_large": "https://s3-media2.fl.yelpcdn.com/assets/2/www/img/d63e3add9901/ico/stars/v1/stars_large_2_half.png",
                                "id": "mac-donalds-paris-4",
                                "is_closed": False
                            },
                            {
                                "is_claimed": True,
                                "rating": 3.5,
                                "mobile_url": "http://m.yelp.com/biz/le-camion-qui-fume-paris?adjust_creative=DhkXE_EgW2WTJ7X-20so4Q&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=DhkXE_EgW2WTJ7X-20so4Q",
                                "rating_img_url": "https://s3-media1.fl.yelpcdn.com/assets/2/www/img/5ef3eb3cb162/ico/stars/v1/stars_3_half.png",
                                "review_count": 156,
                                "name": "Le Camion Qui Fume",
                                "rating_img_url_small": "https://s3-media1.fl.yelpcdn.com/assets/2/www/img/2e909d5d3536/ico/stars/v1/stars_small_3_half.png",
                                "url": "http://www.yelp.com/biz/le-camion-qui-fume-paris?adjust_creative=DhkXE_EgW2WTJ7X-20so4Q&utm_campaign=yelp_api&utm_medium=api_v2_search&utm_source=DhkXE_EgW2WTJ7X-20so4Q",
                                "categories": [
                                    [
                                        "Burgers",
                                        "burgers"
                                    ],
                                    [
                                        "Food Trucks",
                                        "foodtrucks"
                                    ]
                                ],
                                "phone": "+33184163375",
                                "snippet_text": "The best Food Truck for Burgers in Paris? I don´t know about that. But damn good Burgers anyway. I liked the Fries too. \n\nPrices are still ok in my book,...",
                                "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/ORecsIAdABLO7oo0kbuuLQ/ms.jpg",
                                "snippet_image_url": "http://s3-media3.fl.yelpcdn.com/photo/7YAKLzYkPqyKwJvSu_cVMg/ms.jpg",
                                "display_phone": "+33 1 84 16 33 75",
                                "rating_img_url_large": "https://s3-media3.fl.yelpcdn.com/assets/2/www/img/bd9b7a815d1b/ico/stars/v1/stars_large_3_half.png",
                                "id": "le-camion-qui-fume-paris",
                                "is_closed": False,
                                "location": {
                                    "city": "Paris",
                                    "display_address": [
                                        "4ème",
                                        "Paris",
                                        "France"
                                    ],
                                    "geo_accuracy": 5.0,
                                    "neighborhoods": [
                                        "4ème",
                                        "Marais"
                                    ],
                                    "country_code": "FR",
                                    "address": [],
                                    "coordinate": {
                                        "latitude": 48.87351,
                                        "longitude": 2.35853
                                    },
                                    "state_code": "75"
                                }
                            }
                        ]
                    }

            return results

        # server.yelp_API_call = _mock_yelp_API_call

    def tearDown(self):
        """Stuff to do after each test."""

        db.session.close()
        db.drop_all()

    def test_signup_fail(self):
        result = self.client.post("/signup",
                                  data={"user_id": 1234,
                                        "phone_number": "1234567890",
                                        "first_name": "Gordon",
                                        "last_name": "Ramsay",
                                        "email": "gramsay@gmail.com",
                                        "password": "123"},
                                  follow_redirects=True)
        self.assertIn("Oops, your email already exists", result.data)

    def test_submit_phone(self):
        result = self.client.post("/submit_phone",
                                  data={"phone_number": 1234567890,
                                        "user_id": 1234},
                                  follow_redirects=True)
        self.assertIn("That number is already taken", result.data)

    # def tests_signin(self):
    #     result = self.client.post("/signup",
    #                               data={"id": 3,
    #                                     "user_id": 7890,
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

    # def test_get_attendee(self):
    #     user_id = 1234

    #     attendee = get_specific_attendee(user_id)
    #     self.assertEqual(attendee[0].is_owner, True)

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
        result = self.client.get("/profile/1234", follow_redirects=True)

        self.assertIn("<em>(1000 characters max.)</em>", result.data)

    def test_get_business(self):
        url = "http://www.afakeurllink.com"

        business = get_specific_business(url)
        self.assertEqual(business.url, "http://www.afakeurllink.com")

    def test_other_user(self):
        result = self.client.get("/other_profile/4321", follow_redirects=True)

        self.assertIn("Joe B", result.data)

    def test_restaurant_query(self):
        result = self.client.post("/restaurant_query",
                                  data={"city": "Paris",
                                        "zipcode": "",
                                        "term": "American",
                                        "distance": 0.000621371},
                                    )
        self.assertIn("Home", result.data)

    # def test_confirmation(self):
        result = self.client.post("/confirmation",
                                  data={"date": "01/01/2018",
                                        "start_time": "01:00",
                                        "end_time": "02:00",
                                        "business_url": "http://www.afakeurllink.com",
                                        "category_id": 1},
                                  )  # how to check a POST with relationship walking?

        self.assertIn("Thanks for creating an event", result.data)

    def test_find_events(self):
        result = self.client.get("/find_events")

        # all events were already matched, so none available

        self.assertIn("<p>Oops! There are currently no events available :\'(</p>\n", result.data)

    def test_matched(self):
        result = self.client.post("/matched",
                                  data={"event_id": "1"},
                                  follow_redirects=True)

        self.assertIn("You have a new meal plan!", result.data)

    def test_upcoming_events(self):
        result = self.client.get("/upcoming_events")

        self.assertIn("Good Eats", result.data)

    def test_profile_edit(self):
        result = self.client.post("/profile-edit",
                                  data={"description": "Hello World"}
                                )

        self.assertIn("You have successfully updated your profile.", result.data)


if __name__ == "__main__":
    unittest.main()

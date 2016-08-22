"""Utility file to seed food databse from Yelp's available categories"""

from model import Category, City, connect_to_db, db
from server import app


def load_categories():
    """Load food categories into database.

       >>> category = Category.query.filter_by(food_type="Dim Sum").first()

       >>> category
       <Event id=21 food_type=Dim Sum>

       >>> category.food_type
       u'Dim Sum'

    """

    specific_food = []

    for category in (open('food_categories.txt')):
        food_type = category.rstrip()
        food_types = food_type.split(' (')
        specific_food.append(food_types[0])

    ordered_specific_food = sorted(specific_food)

    for food_type in ordered_specific_food:

        category = Category(food_type=food_type)
        db.session.add(category)

    db.session.commit()


def load_cities():
    """Load cities into database.

       >>> city = City.query.filter_by(city_name="San Francisco").first()

       >>> city
       <Event id=49 city=San Francisco>

       >>> city.city_name
       u'San Francisco'

    """

    cities = []

    for row in (open('sf_bay_area.txt')):
        city = row.rstrip()
        cities.append(city)

    sorted_cities = sorted(cities)

    for city in sorted_cities:
        city = City(city_name=city)
        db.session.add(city)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

load_categories()
load_cities()

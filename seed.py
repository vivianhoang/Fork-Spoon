"""Utility file to seed food databse from Yelp's available categories"""

from model import Category, City, connect_to_db, db
from server import app


def load_categories():
    """Load food categories into database.

        >>> connect_to_db(app)
        >>> load_categories()
        Categories loaded
        >>> Category.query.all()
        [<Category id=1 food_type=Afghan>, <Category id=2 food_type=American>, <Category id=3 food_type=Asian Fusion>, <Category id=4 food_type=Bagels>, <Category id=5 food_type=Bakeries>, <Category id=6 food_type=Bars>, <Category id=7 food_type=Brazilian>, <Category id=8 food_type=Breakfast & Brunch>, <Category id=9 food_type=Bubble Tea>, <Category id=10 food_type=Buffets>, <Category id=11 food_type=Burgers>, <Category id=12 food_type=Burmese>, <Category id=13 food_type=Cafes>, <Category id=14 food_type=Cambodian>, <Category id=15 food_type=Caribbean>, <Category id=16 food_type=Chinese>, <Category id=17 food_type=Coffee>, <Category id=18 food_type=Comfort Food>, <Category id=19 food_type=Desserts>, <Category id=20 food_type=Dim Sum>, <Category id=21 food_type=Donuts>, <Category id=22 food_type=Eastern European>, <Category id=23 food_type=Ethiopian>, <Category id=24 food_type=Filipino>, <Category id=25 food_type=French>, <Category id=26 food_type=French Southwest>, <Category id=27 food_type=Gastropubs>, <Category id=28 food_type=German>, <Category id=29 food_type=Gluten Free>, <Category id=30 food_type=Hawaiian>, <Category id=31 food_type=Hot Pot>, <Category id=32 food_type=Ice Cream & Frozen Yogurt>, <Category id=33 food_type=Indian>, <Category id=34 food_type=Indonesian>, <Category id=35 food_type=Italian>, <Category id=36 food_type=Japanese>, <Category id=37 food_type=Malaysian>, <Category id=38 food_type=Mediterranean>, <Category id=39 food_type=Mexican>, <Category id=40 food_type=Middle Eastern>, <Category id=41 food_type=Moroccan>, <Category id=42 food_type=Pakistani>, <Category id=43 food_type=Persian/Iranian>, <Category id=44 food_type=Peruvian>, <Category id=45 food_type=Pizza>, <Category id=46 food_type=Pop-Up Restaurants>, <Category id=47 food_type=Portuguese>, <Category id=48 food_type=Ramen>, <Category id=49 food_type=Salad>, <Category id=50 food_type=Sandwiches>, <Category id=51 food_type=Soul Food>, <Category id=52 food_type=Spanish>, <Category id=53 food_type=Steakhouses>, <Category id=54 food_type=Sushi Bars>, <Category id=55 food_type=Swedish>, <Category id=56 food_type=Syrian>, <Category id=57 food_type=Taiwanese>, <Category id=58 food_type=Tapas/Small Plates>, <Category id=59 food_type=Tea>, <Category id=60 food_type=Tex-Mex>, <Category id=61 food_type=Thai>, <Category id=62 food_type=Vegan>, <Category id=63 food_type=Vegetarian>, <Category id=64 food_type=Vietnamese>, <Category id=65 food_type=Waffles>, <Category id=66 food_type=Wine Bars>]
    """

    specific_food = []

    for category in (open('food_categories.txt')):
        food_type = category.rstrip()
        food_types = food_type.split(' (')
        specific_food.append(food_types[0])

    ordered_specific_food = sorted(specific_food)

    for food_type in ordered_specific_food:
        find_food_type = Category.query.filter_by(food_type=food_type).first()
        if not find_food_type:
            category = Category(food_type=food_type)
            db.session.add(category)

    db.session.commit()
    print "Categories loaded"


def load_cities():
    """Load cities into database.

        >>> connect_to_db(app)
        >>> load_cities()
        Cities loaded
        >>> City.query.all()
        [<City id=1 city=Alemeda>, <City id=2 city=Antioch>, <City id=3 city=Atherton>, <City id=4 city=Belmont>, <City id=5 city=Berkeley>, <City id=6 city=Burlingame>, <City id=7 city=Campbell>, <City id=8 city=Colma>, <City id=9 city=Concord>, <City id=10 city=Cupertino>, <City id=11 city=Daly City>, <City id=12 city=Danville>, <City id=13 city=Dublin>, <City id=14 city=East Palo Alto>, <City id=15 city=El Cerrito>, <City id=16 city=Emeryville>, <City id=17 city=Fairfield>, <City id=18 city=Foster City>, <City id=19 city=Fremont>, <City id=20 city=Gilroy>, <City id=21 city=Half Moon Bay>, <City id=22 city=Hayward>, <City id=23 city=Hillsborough>, <City id=24 city=Lafayette>, <City id=25 city=Livermore>, <City id=26 city=Los Altos>, <City id=27 city=Los Gatos>, <City id=28 city=Martinez>, <City id=29 city=Menlo Park>, <City id=30 city=Mill Valley>, <City id=31 city=Millbrae>, <City id=32 city=Milpitas>, <City id=33 city=Morgan Hill>, <City id=34 city=Mountain View>, <City id=35 city=Novato>, <City id=36 city=Oakland>, <City id=37 city=Orinda>, <City id=38 city=Pacifica>, <City id=39 city=Palo Alto>, <City id=40 city=Petaluma>, <City id=41 city=Pittsburg>, <City id=42 city=Pleasanton>, <City id=43 city=Portola Valley>, <City id=44 city=Redwood City>, <City id=45 city=Richmond>, <City id=46 city=Rohnert Park>, <City id=47 city=San Bruno>, <City id=48 city=San Carlos>, <City id=49 city=San Francisco>, <City id=50 city=San Jose>, <City id=51 city=San Leandro>, <City id=52 city=San Mateo>, <City id=53 city=San Pablo>, <City id=54 city=San Rafael>, <City id=55 city=San Ramon>, <City id=56 city=Santa Clara>, <City id=57 city=Santa Rosa>, <City id=58 city=Saratoga>, <City id=59 city=Sonoma>, <City id=60 city=South San Francisco>, <City id=61 city=Suisun City>, <City id=62 city=Sunnyvale>, <City id=63 city=Union City>, <City id=64 city=Vacaville>, <City id=65 city=Vallejo>, <City id=66 city=Walnut Creek>, <City id=67 city=Woodside>]
    """

    cities = []

    for row in (open('sf_bay_area.txt')):
        city = row.rstrip()
        cities.append(city)

    sorted_cities = sorted(cities)

    for city in sorted_cities:
        find_city = City.query.filter_by(city_name=city).first()
        if not find_city:
            city = City(city_name=city)
            db.session.add(city)

    db.session.commit()
    print "Cities loaded"


# if __name__ == "__main__":
    # connect_to_db(app)
#     db.create_all()

# load_categories()
# load_cities()

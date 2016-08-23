from model import connect_to_db, db, User, Event, Attendee, Business, Category, City


def get_specific_event(business_id):
    """Query for event based on business_id being passed in."""

    return Event.query.filter_by(business_id=business_id).first()


def get_specific_attendee(user_id):
    """Query for attendee."""

    return Attendee.query.filter_by(user_id=user_id).all()


def get_specific_user(email):

    return User.query.filter_by(email=email).first()

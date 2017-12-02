import uuid
import datetime

import pymongo
import requests
from src.common.database import Database
import src.models.alerts.constants as AlertConstants
from src.models.items.item import Item

__author__ = 'jslvtr'


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.active = active
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user_email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "We've found a deal! ({}).".format(self.item.url)
            }
        )

    @classmethod
    def find_needing_update(cls, minute_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minute_since_update)
        return (cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                           {"$lte": last_updated_limit}}))

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {'user_email': user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})

    def activate(self):
        self.active = True
        self.save_to_mongo()

    # client = pymongo.MongoClient(Database.URI)
    # Database.DATABASE = client['fullstack']
    # Alert("fuck@shit.com",10,"4e09a95b343d4c608685631c27e32ec0").save_to_mongo()
    # Alert("john@john.com",10,"cd161ff10d7c471a90345c28e8711986").save_to_mongo()
    # Alert("fuck@shit.com",10,"b5702bd52339475c808b6287773f09b1").save_to_mongo()

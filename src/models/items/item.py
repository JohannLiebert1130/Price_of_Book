import re
import uuid

import pymongo
import requests
from bs4 import BeautifulSoup

from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, price=None, image=None, _id=None):
        self.url = url
        self.name = name
        store = Store.find_by_url(url)
        self.price_tag_name = store.price_tag_name
        self.price_query = store.price_query
        self.image_tag_name = store.image_tag_name
        self.image_query = store.image_query
        self.price = price
        self.image = image
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.price_tag_name, self.price_query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group())

        return self.price

    def load_image(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.image_tag_name, self.image_query)
        self.image = element.text.strip()

        return self.image

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))

# client = pymongo.MongoClient(Database.URI)
# Database.DATABASE = client['fullstack']
# Item("WorldWithoutEnd", "http://product.dangdang.com/25158113.html").save_to_mongo()
# Item("ComputerNetworking", "https://www.amazon.cn/dp/B007JFRQ0G").save_to_mongo()
# Item("AmericanGods", "http://product.dangdang.com/24535115.html").save_to_mongo()

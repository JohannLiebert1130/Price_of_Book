import re
import uuid

import requests
from bs4 import BeautifulSoup

from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, _id=None):
        self.url = url
        self.name = name
        store = Store.find_by_url(url)
        print(store)
        tag_name = store.tag_name
        query = store.query
        print(tag_name, query)
        self.price = self.load_price(tag_name, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self, tag_name, query):
        # <span id="priceblock_ourprice" class="a-size-medium a-color-price">$3,299.99</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(tag_name, query)
        string_price = element.text.strip()

        return string_price

    def save_to_mongo(self):
        Database.insert(ItemConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url
        }

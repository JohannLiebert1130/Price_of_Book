import uuid

import pymongo

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors
from src.models.crawlers.crawler import Crawler


class Store(object):
    def __init__(self, name, url_prefix, crawler_id, _id=None):
        self.url_prefix = url_prefix
        self.name = name
        self.crawler = Crawler.get_by_id(crawler_id)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "crawler_id": self.crawler._id
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {"_id": self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        store_data = Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}})
        if store_data is not None:
            return cls(**store_data)
        else:
            return None

    @classmethod
    def find_by_url(cls, url):
        """
        Return a store from a ur
        :param url: The item's url
        :return: a Store, or roaises a StoreNotFoundException if  no store matches the URL
        """
        try:
            for i in range(len(url) - 5, -1, -1):
                #print(url[:i])
                store = cls.get_by_url_prefix(url[:i])
                if store is not None:
                    return store
        except:
            raise StoreErrors.StoreNotFoundException("The URL prefix used to find the store"
                                                     " didn't give us any results!")

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})
        self.crawler.delete()


# client = pymongo.MongoClient(Database.URI)
# Database.DATABASE = client['fullstack']
# Store("dangdang", "http://product.dangdang.com", "p", {"id": "dd-price"}).save_to_mongo()
# Store("AmazonCN", "https://www.amazon.cn/", "span", {"class": "a-size-base a-color-price a-color-price"}).save_to_mongo()

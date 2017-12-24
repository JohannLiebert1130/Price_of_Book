import uuid

from src.common.database import Database
import src.models.crawlers.constants as CrawlerConstants


class Crawler(object):
    def __init__(self, price_tag_name, price_query, image_tag_name, image_query, _id=None):
        self.price_query = price_query
        self.price_tag_name = price_tag_name

        self.image_tag_name = image_tag_name
        self.image_query = image_query

        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(CrawlerConstants.COLLECTION, {"_id": _id}))

    def json(self):
        return {
            "price_query": self.price_query,
            "price_tag_name": self.price_tag_name,
            "image_query": self.image_query,
            "image_tag_name": self.image_tag_name,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.update(CrawlerConstants.COLLECTION, {"_id": self._id}, self.json())

    def delete(self):
        Database.remove(CrawlerConstants.COLLECTION, {'_id': self._id})

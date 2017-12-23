from src.common.database import Database
import src.models.crawlers.constants as CrawlerConstants


class Crawler(object):
    def __init__(self, price_tag_name, price_query, image_tag_name, image_query, description_tag_name, description_query, store_id):
        self.price_query = price_query
        self.price_tag_name = price_tag_name
        self.image_tag_name = image_tag_name
        self.image_query = image_query
        self.description_tag_name = description_tag_name
        self.description_query = description_query
        self.store_id = store_id

    @classmethod
    def find_by_store(cls, store_id):
        return cls(**Database.find_one(CrawlerConstants.COLLECTION, {"store_id": store_id}))

    def json(self):
        return {
            "price_query": self.price_query,
            "price_tag_name": self.price_tag_name,
            "image_query": self.image_query,
            "image_tag_name": self.image_tag_name,
            "description_query": self.description_query,
            "description_tag_name": self.description_tag_name,
            "store_id": self.store_id
        }

    def save_to_mongo(self):
        Database.update(CrawlerConstants.COLLECTION, {"store_id": self.store_id}, self.json())
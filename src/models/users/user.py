import uuid

import pymongo

from src.common.database import Database
from src.common.utils import Utils
from src.models.alerts.alert import Alert
from src.models.users import errors
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_valid_login(email, password):
        """
        This method verifies that an email/password combo is valid or not.
        Check that the email exists, and that the password associated to that email is valid.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email})  # password in sha512->pbkdf2_sha512
        if user_data is None:
            raise errors.UserNotExistsError("Your user is not exist.")
            return False
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise errors.IncorrectPasswordError("Your password is wrong.")
            return False
        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using email and password.
        The password already comes hashed as sha-512.
        :param email: user's email (might be invalid)`
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            # Tell user they are already registered
            raise errors.UserAlreadyRegisteredError("The email you used to register already exists.")
        if not Utils.email_is_valid(email):
            # Tell user that their email is not constructed properly.
            raise errors.InvalidEmailError("The email does not have the right format.")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    def save_to_db(self):
        Database.insert(collection=UserConstants.COLLECTION,
                        query=self.json())

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)

# client = pymongo.MongoClient(Database.URI)
# Database.DATABASE = client['fullstack']
# # User.register_user("fuck@shit.com", "fuckshit")
# # User.register_user("john@john.com", "john")
# user = User.find_by_email("fuck@shit.com")
# bool = User.is_valid_login("fuck@shit.com", "fckshit")
# print(bool)

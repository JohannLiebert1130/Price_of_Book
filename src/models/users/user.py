import uuid

from src.common.database import Database
from src.common.utils import Utils
from src.models.users import errors


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

        user_data = Database.find_one('users', {'email': email})  # password in sha512->pbkdf2_sha512
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

        user_data = Database.find_one("users", {"email": email})

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
        Database.insert(collection='users',
                        query=self.json())

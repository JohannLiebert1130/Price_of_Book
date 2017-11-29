import uuid

from src.common.database import Database
from src.common.utils import Utils
from src.models.users.errors import UserNotExistsError, IncorrectPasswordError


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
            raise UserNotExistsError("Your user is not exist.")
            return False
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise IncorrectPasswordError("Your password is wrong.")
            return False
        return True

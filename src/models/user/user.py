from dataclasses import dataclass, field
from uuid import uuid4
from typing import Dict, List

from common.database import Database
from common.utils import Utils
from models.model import Model
import models.user.errors as UserErrors

@dataclass
class User(Model):
    collection: str = field(default='users', init=False)
    email: str
    password: str = field(repr=False)
    _id: str = field(default_factory=lambda: uuid4().hex)

    def json(self) -> Dict:
        return {
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }

    @classmethod
    def find_by_email(cls, email: str):
        try:
            return cls.find_one_by("email", email)
        except TypeError:
            raise UserErrors.UserNotFoundError('No user found attached to that e-mail.')

    @classmethod
    def validate_register(cls, email: str, password: str) -> bool:
        if not Utils.validate_email(email):
            raise UserErrors.InvalidEmailError('Invalid e-mail format.')
        """
        if not Utils.validate_password(password):
            raise UserErrors.InvalidPasswordError('Invalid password format.')
        """
        try:
            cls.find_by_email(email)
        except UserErrors.UserNotFoundError:
            User(email, password).save_to_mongo()
            return True
        return UserErrors.UserNotFoundError

    @classmethod
    def validate_login(cls, email: str, password: str) -> bool:
        try:
            cls.find_by_email(email)
            return True
        except UserErrors.UserNotFoundError:
            return False

from dataclasses import dataclass, field
from uuid import uuid4
from typing import Dict

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
        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('There is an account already registered to that email.')
        except UserErrors.UserNotFoundError:
            if not Utils.validate_password(password):
                raise UserErrors.InvalidPasswordError('Invalid password format.')
            User(email, Utils.hash_password(password)).save_to_mongo()
            return True

    @classmethod
    def validate_login(cls, email: str, password: str) -> bool:
        user = cls.find_by_email(email)
        if not user:
            raise UserErrors.UserNotFoundError('User not found.')
        if not Utils.verify_password(password, user.password):
            raise UserErrors.PasswordEmailNotMatching('Password does not match the account attached to this email.')
        return True

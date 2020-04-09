import re
from passlib.hash import pbkdf2_sha512

class Utils:
    @staticmethod
    def validate_email(email: str) -> bool:
        email_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_matcher.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def verify_password(password: str, hash_password: str) -> bool:
        return pbkdf2_sha512.verify(password, hash_password)

import re


class Utils():
    @staticmethod
    def validate_email(email: str) -> bool:
        email_matcher = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')

        return True if email_matcher.match(email) else False

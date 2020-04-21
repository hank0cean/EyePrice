import os
from requests import Response, post
from typing import List

class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message

class Mailgun: 
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY", None)
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN", None)

    NO_REPLY_EMAIL = "no-reply@eyeprice.com"
    NO_REPLY_TITLE = "EyePrice - Do Not Reply"

    @classmethod
    def send_email(cls, user_email: List[str], subject: str, text: str, html: str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException("Could not load Mailgun API key.")
        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException("Could not load Mailgun Domain.")
        response = post(f"{cls.MAILGUN_DOMAIN}/messages",
                        auth=("api", f"{cls.MAILGUN_API_KEY}"),
                        data={"from": f"{cls.NO_REPLY_TITLE} <{cls.NO_REPLY_EMAIL}>",
                              "to": f"{user_email}",
                              "subject": f"{subject}",
                              "text": f"{text}",
                              "html": f"{html}"})
        if response.status_code != 200:
            raise MailgunException("Error occurred while trying to send e-mail.")
        return response

import jwt
import datetime
import calendar
from flask import abort

from constants import SECRET, ALGO

from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            abort(404)
        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(404)

        data = {
            'email': email,
            'password': password,
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)

        days30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data["exp"] = calendar.timegm(days30.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        return {
            "access_token": access_token,
            "refresh_token":  refresh_token
        }

    def refresh_token(self, token):
        data = jwt.decode(jwt=token, key=SECRET, algorithms=[ALGO])
        username = data.get('email')

        return self.generate_token(username, None, is_refresh=True)



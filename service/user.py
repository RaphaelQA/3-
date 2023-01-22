import base64
import hashlib
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_user_by_id(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, usernane):
        return self.dao.get_user_by_username(usernane)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS).decode("utf-8", "ignore")

    def compare_passwords(self, hash, password) -> bool:
        return hmac.compare_digest(
            base64.b64decode(hash),
            hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        )

    def create(self, u_data):
        u_data['password'] = self.get_hash(u_data['password'])

        return self.dao.create(u_data)

    def update(self, u_data):
        u_data['password'] = self.get_hash(u_data['password'])

        return self.dao.update(u_data)
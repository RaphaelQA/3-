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

    def get_by_email(self, email):
        return self.dao.get_user_by_email(email)

    def delete(self, uid):
        return self.dao.delete(uid)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)
        return base64.b64encode(hash_digest)

    def compare_passwords(self, hash, password):
        decode_dipest = base64.b64decode(hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decode_dipest, hash_digest)

    def create(self, u_data):
        u_data['password'] = self.get_hash(u_data['password'])

        return self.dao.create(u_data)

    def update(self, u_data):
        u_data['password'] = self.get_hash(u_data['password'])

        return self.dao.update(u_data)

    def update_pass(self, u_data):
        return self.dao.updade_pass(u_data)
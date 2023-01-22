from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_user_by_id(self, uid):
        return self.session.query(User).get(uid)

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, data):
        user = User(**data)

        self.session.add(user)
        self.session.commit()

        return user

    def update(self, data):
        user = self.get_user_by_id(data.get('id'))
        user.username = data.get('username')
        user.password = data.get('password')
        user.role = data.get('role')

        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_user_by_id(uid)

        self.session.delete(user)
        self.session.commit()

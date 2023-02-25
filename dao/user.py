from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_user_by_id(self, uid):
        return self.session.query(User).get(uid)

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def create(self, data):
        user = User(**data)

        self.session.add(user)
        self.session.commit()

        return user

    def update(self, data):
        user = self.get_user_by_id(data.get('id'))
        user.email = data.get('email')
        user.name = data.get('name')
        user.surname = data.get('surname')
        user.favorite_genre = data.get('favorite_genre')

        self.session.add(user)
        self.session.commit()

    def updade_pass(self, data):
        user = self.get_user_by_id(data.get('id'))
        user.password = data.get('password')
        self.session.add(user)
        self.session.commit()

    def delete(self, uid):
        user = self.get_user_by_id(uid)

        self.session.delete(user)
        self.session.commit()

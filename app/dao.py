from app.models import User
from app import app, db
import hashlib
import cloudinary.uploader


# NOTE: ADD ARRANGEMENT FUNCTION(), ...

def auth_user(phone, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(phone), User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_user(name, username, password, phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password, phone=phone)

    db.session.add(u)
    db.session.commit()

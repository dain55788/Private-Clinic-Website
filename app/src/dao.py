from app.src.models import User
from app.src.models import Arrangement

from app import db
import hashlib


# import cloudinary.uploader


# NOTE: ADD ARRANGEMENT FUNCTION(), ...

def auth_user(phone, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.phone.__eq__(phone), User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def get_user_by_id(id_patient):
    return User.query.get(id_patient)


def add_user(name, username, gender, password, phone):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, gender=gender, password=password, phone=phone)

    db.session.add(u)
    db.session.commit()


def check_user_phone(phone):
    u = User.query.filter(User.phone.__eq__(phone))
    user_id = u.get_id()
    return user_id


def add_arrangement(id_patient, phone, name, appointment_date, address, description,  id_nurse=None):
    id_patient = check_user_phone(phone)
    arr = Arrangement(phone=phone, patient_name=name,
                      appointment_date=appointment_date, address=address, description=description)

    db.session.add(arr)
    db.session.commit()


def check_unique_phone(phone):
    user = db.session.query(User).filter_by(phone=phone).first()

    return user is None  # True if no user found, i.e., phone is unique

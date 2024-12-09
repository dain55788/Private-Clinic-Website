from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
    DOCTOR = 3
    NURSE = 4


class User(db.Model, UserMixin):
    id_patient = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    arrangements = relationship('Arrangement', backref='user', lazy=True)  # Backref tới bảng Arrangement


class Category(db.Model):
    id_cate = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    arrangements = relationship('Arrangement', backref='category', lazy=True)


class Arrangements(db.Model):
    id_arr = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    arrangements = relationship('Arrangement', backref='arrangements', lazy=True)


class Arrangement(db.Model):
    id_arragement = Column(Integer, primary_key=True, autoincrement=True)
    id_patient = Column(Integer, ForeignKey(User.id_patient), nullable=False)  # Khóa ngoại tham chiếu User.id_patient
    id_cate = Column(Integer, ForeignKey(Category.id_cate), nullable=False)
    id_arr_list = Column(Integer, ForeignKey(Arrangements.id_arr), nullable=False)
    # appointment_date = Column(datetime, nullable=False)
    description = Column(String(255), nullable=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


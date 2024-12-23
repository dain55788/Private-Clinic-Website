from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum, Date
from sqlalchemy.orm import relationship
from app import db, app
from enum import Enum as RoleEnum
import hashlib
from flask_login import UserMixin
import datetime
from datetime import datetime


# NOTE: SỬA LẠI TOÀN BỘ CSDL, CÁC BẢNG USER, ARRANGEMENTS, ARR_LISTS, test với các data


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2  # Patient
    DOCTOR = 3
    NURSE = 4


class User(db.Model, UserMixin):
    id_patient = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=False, unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    arrangement = relationship('Arrangement', backref='user', lazy=True)  # Backref tới bảng Arrangement

    def get_id(self):
        return self.id_patient


class ArrList(db.Model):
    id_arr_list = Column(Integer, primary_key=True, autoincrement=True)
    appointment_date = Column(Date, nullable=False)
    patient_quantity = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    arrangement = relationship('Arrangement', backref='arrlist', lazy=True)


class Arrangement(db.Model):
    id_arrangement = Column(Integer, primary_key=True, autoincrement=True)
    id_arr_list = Column(Integer, ForeignKey(ArrList.id_arr_list), nullable=True)
    id_patient = Column(Integer, ForeignKey(User.id_patient), nullable=False)  # Khóa ngoại tham chiếu User.id_patient
    id_nurse = Column(Enum(UserRole), default=UserRole.NURSE, nullable=True)  # nullable
    phone = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    gender = Column(String(50), nullable=False)
    patient_name = Column(String(50), nullable=False)
    appointment_date = Column(Date, nullable=False)
    address = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # create all the defined tables above

        # import hashlib
        #
        # users = [{
        #     "name": "nguyen dai nurse",
        #     "username": "nurse",
        #     "gender": "Nữ",
        #     "password": str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     "phone": "0903021744",
        #     "user_role": UserRole.NURSE
        # }, {
        #     "name": "nguyen dai",
        #     "username": "patient123",
        #     "gender": "Nam",
        #     "password": str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     "phone": "0903214124",
        #     "user_role": UserRole.USER
        # }, {
        #     "name": "nguyen dai doctor",
        #     "username": "doctor",
        #     "gender": "Nam",
        #     "password": str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #     "phone": "0903021746",
        #     "user_role": UserRole.DOCTOR
        # }]
        # delete all users, arr_lists, arrangements before adding
        # db.session.query(Arrangement).delete()
        # db.session.query(ArrList).delete()
        # db.session.query(User).delete()

        # # adding users session
        # for u in users:
        #     user = User(**u)
        #     db.session.add(user)
        # db.session.commit()

        # import pytz
        #
        # test_date = datetime.now()

        # add patient id to arrangements
        # test_user2 = User(name="Nguyen Dai", username="apache spark", password="12345", phone="0903021731")
        # test_user3 = User(name="Tom Hardy", username="venom", password="12345", phone="0128012924")
        #
        # db.session.add_all([test_user2, test_user3])
        # db.session.commit()
        # user2_id = test_user2.id_patient
        # user3_id = test_user3.id_patient
        #
        # arrangements = [{
        #     "id_patient": user2_id,
        #     "appointment_date": test_date,
        #     "description": "het cuu",
        # }, {
        #     "id_patient": user3_id,
        #     "appointment_date": test_date,
        #     "description": "het cuu",
        # }]
        #
        # for arr in arrangements:
        #     arrangement = Arrangement(**arr)
        #     db.session.add(arrangement)

        db.session.commit()

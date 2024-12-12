import math

from flask import render_template, request, redirect, jsonify, session
import dao
from app import app, login
from flask_login import login_user, logout_user, login_required
from app.models import User, UserRole


@app.route("/")
def index():
    return render_template('mainPage.html')


@app.route("/login", methods=['get', 'post'])
def login_process():
    if request.method.__eq__('POST'):
        phone = request.form.get('phone')
        password = request.form.get('password')

        user = dao.auth_user(phone=phone, password=password)
        if user:
            login_user(user=user)
            return redirect('/')

    return render_template('login.html')


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/')


@app.route("/register", methods=['get', 'post'])
def register_process():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            data = request.form.copy()
            # ADD the function to check if the "Điều khoản" button is clicked

            del data['confirm']

            dao.add_user(**data)
            return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route("/user_arrangement")
def user_arrangement():
    return render_template('user_arrangement.html')


# Handling case of user login
login.login_view = 'login_process'


@app.route("/dangKyLich")
@login_required
def dangKyLich():
    return render_template('dangKyLich.html')


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)


def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)

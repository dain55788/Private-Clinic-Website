from flask import render_template, request, redirect
import dao
from app import app, login
from flask_login import login_user, logout_user, login_required, current_user
from app.src.models import User


@app.route("/")
def index():
    return render_template('mainPage.html')


@app.route("/login", methods=['get', 'post'])
def login_process():
    err_msg = None
    err_msg1 = None
    if current_user.is_authenticated:
        return redirect('/')
    if request.method.__eq__('POST'):
        phone = request.form.get('phone')
        password = request.form.get('password')
        if not phone or not password:
            err_msg = '*Vui lòng nhập đầy đủ thông tin!!'
        else:
            user = dao.auth_user(phone=phone, password=password)
            if user:
                login_user(user=user)
                return redirect('/')
            else:
                err_msg1 = '*Số điện thoại hoặc mật khẩu KHÔNG khớp!!'

    return render_template('login.html', err_msg=err_msg, err_msg1=err_msg1)


@app.route("/logout")
def logout_process():
    logout_user()
    return redirect('/')


@app.route("/register", methods=['get', 'post'])
def register_process():
    err_msg = None
    err_msg1 = None # len(password) >= 8
    err_msg2 = None # empty fullname and usernane field
    err_msg3 = None
    err_msg4 = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        username = request.form.get('username')
        gender = request.form.get('gender')
        fname = request.form.get('name')
        phone = request.form.get('phone')
        if not username or not fname or not gender:
            err_msg2 = '*Vui lòng nhập đầy đủ thông tin!!'
        elif not password or len(password) < 8:
            err_msg1 = '*Mật khẩu có độ dài tối thiểu là 8!!'
        elif not password.__eq__(confirm):
            err_msg = '*Mật khẩu KHÔNG khớp!!'
        elif not request.form.get('accept-terms'):
            err_msg3 = '*Bạn cần chấp nhận Điều khoản sử dụng!!'
        elif not dao.check_unique_phone(phone):
            err_msg4 = '*Số điện thoại đã được sử dụng!!'
        else:
            data = request.form.copy()
            # ADD the function to check if the "Điều khoản" button is clicked

            del data['confirm']
            del data['accept-terms']
            dao.add_user(**data)
            return redirect('/login')

    return render_template('register.html', err_msg=err_msg, err_msg1=err_msg1,
                           err_msg2=err_msg2, err_msg3=err_msg3, err_msg4=err_msg4)


@app.route("/user_arrangement")
def user_arrangement():
    return render_template('user_arrangement.html')


# Handling case of user login
login.login_view = 'login_process'


@app.route("/dangKyLich")
@login_required
def dang_ky_lich():  # chưa xử lý ràng buộc về quy định số bệnh nhân trong ngày
    err_msg = None
    # err_msg1 = None
    # err_msg2 = None  # empty fullname field
    #
    if request.method.__eq__('POST'):
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        fname = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('appointment_date')
        if not fname or not gender or not phone or not date or not email:
            err_msg = '*Vui lòng nhập đầy đủ thông tin!!'
        # else:
        #     data = request.form.copy()
        #
        #     dao.add_arrangement(**data)
        #     return redirect('/login')
    return render_template('dangKyLich.html')


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(user_id)


def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)

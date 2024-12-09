from flask import render_template, request, Flask
from app import app


@app.route("/")
def index():
    return render_template('mainPage.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/dangKyLich")
def dangKyLich():
    return render_template('dangKyLich.html')


if __name__ == '__main__':
    app.run(debug=True)



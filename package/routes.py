from flask import render_template, request, redirect, session, url_for, jsonify, flash
import bcrypt

# from package import db, app, Size
from flask_login import login_user, logout_user, login_required, current_user

from package import Size, app, User, menu
from package.defs import *
# from package.models import Vehicle, User


@app.route('/db', methods=['POST', 'GET'])
@login_required
def db():
    return 'You are logged in'


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", title='Main page title', menu=menu)


@app.route("/login", methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    next_page = request.args.get('next')

    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and str.encode(user.password) == bcrypt.hashpw(str.encode(password), str.encode(user.salt)):
            login_user(user)
            return url_for('profile_old', user_id=user.user_id)
        else:
            flash('Email or password is not correct', 'error')
    else:
        flash('Fill in email and password')

    return render_template("login.html", title='Login page', menu=menu)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['password']) > 4 and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['psw'])
            res = db.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html", title="Register", menu=menu)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        print(request.url)
        link = url_for('login') + '?next=' + request.url
        print(link)
        return redirect(link)
    return response


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", title="Профиль", menu=menu)


@app.route('/profile/<user_id>')
@login_required
def profile_old(user_id):
    print('user_id ', user_id)
    print('current_user ', current_user.user_id)
    if user_id == current_user.user_id:
        res = User.query.filter_by(user_id=user_id).first().first_name
        return res
    else:
        return redirect(url_for('login'))

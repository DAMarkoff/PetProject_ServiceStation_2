from flask import render_template, request, redirect, session, url_for, jsonify

from package import app, db, Vehicle, Users
from package.defs import *


@app.route('/db', methods=['POST', 'GET'])
def insert():
    new_vehicle = Vehicle(vehicle_name='spaceship')
    db.session.add(new_vehicle)
    db.session.commit()

    res = db.session.query(Vehicle).all()
    # for r in res:
    #     print(r.vehicle_name)
    return res


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if 'userLogged' in session:
            return redirect(url_for('profile', user_id=session['userLogged']))
        elif request.form['email'] == 'dan@dan.us' and request.form['password'] == 'aa':
            session['userLogged'] = request.form['email']
            return redirect(url_for('profile', user_id=session['userLogged']))

    return render_template("login.html")


@app.route('/profile/<user_id>')
def profile(user_id):
    if 'userLogged' not in session or session['userLogged'] != user_id:
        abort(401)

    res = db.session.query(Users).filter_by(email=user_id).first()

    print(res)
    return ''


@app.route("/users/login", methods=['POST'])
def users_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        required_fields = {
            'email': email,
            'password': password
        }
        check_required_fields(required_fields)

        check_user_exists('does not exist', email)
        check_db_connection()

        if not get_value_from_table('active', 'users', 'email', email):
            abort(400, description='The user is deactivated')

        sql_query = "SELECT salt, user_id, first_name, last_name, password FROM users WHERE email = '{0}'".format(email)
        cursor.execute(sql_query)
        conn.commit()
        # res = cursor.fetchone()
        salt, user_id, first_name, last_name, password_db = cursor.fetchone()

        if password_is_valid(salt, password, password_db):
            # if r.exists(email) == 0:
            #     token = str(uuid.uuid4())
            #     r.set(email, token, ex=600)
            # else:
            #     token = r.get(email)
            #     r.expire(email, 600)

            # Hello message (For fun :)
            text = 'Hello, {{ name }}!'
            template = Template(text)

            result = {
                "hello_message": template.render(name=first_name + " " + last_name),
                "token": token,
                "email": email,
                "user_id": user_id
            }
            return jsonify(result)
        else:
            abort(401, description='you shall not pass :) password is invalid')
    else:
        abort(405)
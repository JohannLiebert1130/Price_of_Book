from flask import Flask, Blueprint, request, session, redirect, url_for, render_template

from src.models.users.errors import UserError
from src.models.users.user import User

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route("/login", methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        try:
            if User.is_valid_login(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserError as e:
            return e.message

    return render_template("users/login.jinja2")  # send the user an error if their login was invalid.


@user_blueprint.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for(".user_alerts"))
        except UserError as e:
            return e.message

    return render_template("users/register.jinja2")  # send the user an error if their login was invalid.


@user_blueprint.route("/alerts")
def user_alerts():
    return 'This is the alerts page.'


@user_blueprint.route("/logout")
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


@user_blueprint.route("/check_alerts/<string:user_id>")
def check_user_alerts(user_id):
    pass

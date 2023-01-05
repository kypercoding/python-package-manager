import argparse
import requests
import urllib.parse as urlp
import json
import secrets
import os

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

import cache
from user import User


# app instance
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# set configurations
HOST = os.environ.get("HOST") if not None else None
PORT = int(os.environ.get("PORT")) if os.environ.get("PORT") is not None else None
DB_NUM = int(os.environ.get("PORT")) if os.environ.get("PORT") is not None else None

# base url declaration
BASE_URL = os.environ.get("BASE_URL")

# database configs
app.config['db'] = {
    'host': HOST,
    'port': PORT,
    'db': DB_NUM
}

# generate secret
app.secret_key = os.environ.get("APP_SECRET")

# login manager
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

###
#
# Routes for handling user login, registration, and verification.
#
###

# route for handling requests to homepage
@app.route('/', methods=["GET"])
def index():
    """
    Redirects a user to the home page.
    """
    return render_template("index.html")


# route for handling login page request
@app.route('/login', methods=["GET"])
def login():
    """
    Redirects a user to the login page.
    """
    return render_template("login.html")


# logs user into the actual application
@app.route("/authenticate", methods=["POST"])
def authenticate():
    """
    Authenticate user by calling the REST API.
    """

    # get username and password credentials
    data = {
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }

    url = str(urlp.urljoin(BASE_URL, "/login"))

    # put username and password in body of request
    response = requests.post(url, data=data)

    # if response code is not 200 or 201, then have the user log in again;
    # otherwise, set a Flask session with the JWT tokens and go to the
    # environments
    if response.status_code != 200 and response.status_code != 201:
        return redirect("/login")

    # save JWT token to quick Flask session
    tokens = json.loads(response.content)

    # create user object
    user = User(data['username'], tokens['accessToken'], tokens['refreshToken'])

    # add user to Redis cache
    cache.set_user_tokens(user, app.config['db'])

    # log user in
    login_user(user)

    return redirect("/home")


# route for handling registration page request
@app.route('/registration', methods=["GET"])
def registration():
    """
    Redirects a user to the registration page.
    """
    return render_template("registration.html")


# registers a user with the API
@app.route('/register', methods=["POST"])
def register():
    """
    Registers a user to the API.
    """

    # get username and password credentials
    data = {
        "username": request.form.get("username"),
        "password": request.form.get("password")
    }

    url = str(urlp.urljoin(BASE_URL, "/register"))

    # put username and password in body of request
    response = requests.post(url, data=data)

    # if response code is not 200 or 201, then have the user log in again;
    # otherwise, set a Flask session with the JWT tokens and go to the
    # environments
    if response.status_code != 200 or response.status_code != 201:
        return redirect("/registration")

    return redirect("/login")


###
#
# Routes for handling functions inside the application itself.
#
###

@app.route("/home", methods=["GET"])
@login_required
def home():
    """
    Go to the home dashboard for environments.
    """

    # construct url to get user's environments
    url = str(urlp.urljoin(BASE_URL, "/environments"))

    # construct request with JWT tokens
    data = requests.get(url, headers={"authorization": "access_token {}".format(
        cache.get_access_token(current_user.get_id(), app.config['db']).decode()
    )})

    # convert JSON to list of dictionaries
    environments = json.loads(data.content)

    return render_template("/home.html", environments=environments)


@app.route("/delete-environments", methods=["POST"])
@login_required
def delete_environments():
    """
    Delete all environments associated with user.
    """

    # construct url to get user's environments
    url = str(urlp.urljoin(BASE_URL, "/environments/delete-environments"))

    # construct request with JWT tokens
    requests.delete(url, headers={"authorization": "access_token {}".format(
        cache.get_access_token(current_user.get_id(), app.config['db']).decode()
    )})

    return redirect("/home")


@app.route("/add-environment", methods=["POST"])
@login_required
def add_environment():
    """
    Add environment associated with user.
    """

    # get the name and environment type
    name = request.form.get("name")
    env_type = "python"

    # put data into JSON-like dictionary
    data = {
        "name": name,
        "envType": env_type
    }

    # construct url to get user's environments
    url = str(urlp.urljoin(BASE_URL, "/environments/add-environment"))

    # make request
    requests.post(url, data=data, headers={"authorization": "access_token {}".format(
        cache.get_access_token(current_user.get_id(), app.config['db']).decode()
    )})

    return redirect("/home")


@app.route("/add-packages", methods=["POST"])
@login_required
def add_packages():
    """
    Add packages to an given environment.
    """

    # get the envID and the packages desired
    packages_str = request.form.get("packages")
    env_id = request.form.get("env_id")

    # split packages input by whitespace into separate packages
    packages = packages_str.split()

    # create data
    data = {
        "envID": env_id,
        "packages": packages
    }

    # construct url
    url = str(urlp.urljoin(BASE_URL, "/environments/add-packages"))

    # make request
    requests.put(url, data=data, headers={"authorization": "access_token {}".format(
        cache.get_access_token(current_user.get_id(), app.config['db']).decode()
    )})

    return redirect("/home")


# user loader
@login_manager.user_loader
def load_user(id):
    """
    Load user into the login manager.
    """

    access_token = cache.get_access_token(id, app.config['db'])
    refresh_token = cache.get_access_token(id, app.config['db'])

    return User(id, access_token, refresh_token)


# log out
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Log user out.
    """

    cache.unset_user_tokens(current_user, app.config['db'])

    logout_user()

    return redirect("/")


if __name__ == '__main__':
    # obtains host, username, password, database, and port from
    # command line for testing purposes only
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="Base URL for API", type=str)
    parser.add_argument('host', help="Host for Redis development server", type=str)
    parser.add_argument('port', help="Port for Redis development server", type=int)
    parser.add_argument('db', help="Database for Redis development server", type=int)

    # parse arguments
    args = parser.parse_args()

    # set base url
    BASE_URL = args.base_url

    # set database configurations
    db = {
        'host': args.host,
        'port': args.port,
        'db': args.db
    }

    app.config['db'] = db

    # generate secret key for testing
    app.secret_key = secrets.token_urlsafe(32)

    app.run(debug=True)

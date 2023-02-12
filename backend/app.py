import os
import random
import string
import traceback

from flask import Flask, jsonify, request,session, Response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv


from util.my_logger import my_logger
from my_model import user_model
from provider.baseball_scrapper import get_baseball_rank

# instantiate the app
app = Flask(__name__)
app.secret_key = 'laksdjfoiawjewfansldkfnzcvjlzskdf'

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
db = SQLAlchemy()
db.init_app(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
# 비밀번호 암호화
bcrypt = Bcrypt(app)


# sanity check route
@app.route('/', methods=['GET'])
def test_router():
    my_logger.info("hello this is root url!")
    return jsonify('This is Docker Test developments Server!')


@app.route('/health_check', methods=['GET'])
def health_check():
    my_logger.info("hello this is root url!")
    return jsonify('good')


@app.route('/main_btn', methods=['GET'])
def main_btn():
    my_logger.info("click Main Btn")
    data = []
    string_pool = string.ascii_lowercase
    result_dict = {}

    for i in range(15):
        result_val = ''

        for j in range(10):
            result_val += random.choice(string_pool)

        result_dict['key'] = result_val

        data.append(result_dict)

    return jsonify(data)


@app.route("/api/auth/signup", methods=['POST'])
def auth_signup():
    my_logger.info("SignUp!")
    my_logger.info(request.get_json())

    data = request.get_json()

    username = data.get('username')
    useremail = data.get('useremail')
    userpwd = data.get('userpwd')
    bio = data.get('bio')

    user_data = user_model.User.query.filter_by(username=username).first()
    if user_data is not None:
        my_logger.info("Username is Already exist")
        return {"success": "username is already exist"}

    try:
        user = user_model.User(**data)
        user.has_password()
        user_model.db.session.add(user)
        user_model.db.session.commit()
        user_model.db.session.remove()
        my_logger.info("user Save Success")
    except Exception as e:
        my_logger.error("user Save Fail")
        my_logger.debug(traceback.print_exc(e))
        return {'fail': "user Save Fail"}


@app.route("/api/auth/login", methods=['POST'])
def auth_login():
    my_logger.info("User auth Login")
    my_logger.info(request.get_json())

    username = request.get_json()['username']
    useremail = request.get_json().get('useremail')
    userpwd = request.get_json()['userpwd']

    my_user = user_model.User()

    try:
        user_data = my_user.query.filter_by(username=username).first()

        if user_data is not None:
            my_logger.info(user_data.userpwd)
            auth = user_data.check_password(userpwd)
            if not auth:
                my_logger.info("password validation fail!")
                return {'success': 'password validation fail!'}
            else:
                my_logger.info("login success!")
                session['login'] = True
                return {'success': 'user Login Success!'}
        else:
            my_logger.info("user information is wrong or user does not exists....")
            session['login'] = False
            return {'success': 'user information is wrong or user does not exists....'}
    except Exception as e:
        my_logger.error("login Exception...")
        my_logger.debug(traceback.print_exc(e))
        session['login_session'] = False
        return {'fail': 'login Exception...'}


@app.route('/app/auth/logout')
def auth_logout():
    session['login_session'] = False
    return {'success': 'logout'}


@app.route('/baseball_data', methods=['GET'])
def baseball_data():
    my_logger.info("baseball_data route!!")
    data_list = get_baseball_rank()
    return jsonify(data_list)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'), debug=os.environ.get('FLASK_DEBUG'))

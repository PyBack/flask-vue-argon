import os
import random
import string
import traceback
import requests

from flask import Flask, jsonify
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
    result_dict={}

    for i in range(15):
        result_val = ''

        for j in range(10):
            result_val += random.choice(string_pool)

        result_dict['key'] = result_val

        data.append(result_dict)

    return jsonify(data)


@app.route("/api/auth/signup", method=['POST'])
def auth_signup():
    my_logger.info("SignUp!")
    my_logger.info(requests.get_json())

    data = requests.get_json()

    username = data.get('username')
    useremail = data.get('useremail')
    userpwd = data.get('userpwd')
    bio = data.get('bio')


@app.route('/baseball_data', methods=['GET'])
def baseball_data():
    my_logger.info("baseball_data route!!")
    data_list = get_baseball_rank()
    return jsonify(data_list)


if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'), debug=os.environ.get('FLASK_DEBUG'))

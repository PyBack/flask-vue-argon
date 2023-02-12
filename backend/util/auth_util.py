import jwt
from flask import request, jsonify, current_app
from my_model.user_model import User
from util.my_logger import my_logger
from functools import wraps


def token_required(f):
    """
    데이터 생성/조회를 위한 권한 부여를 위한 데코레이터
    토큰을 생성하고, 확인하는 작업, 이제 어떤 라우터에서든, 위의 모듈을 import 하고
    데코레이터 형태로 사용하면 인증이 필요한 절차가 된다.
    """
    @wraps(f)
    def _verify(*args, **kwars):
        auth_headers = request.headers.get("Authorization", '').split()

        invalid_msg = {
            'message': 'Invalid Token. Registeration / authentication required',
            'authenticated': False
        }

        expired_msg = {
            'message': 'expired Token. Reauthentication required',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401
        try:
            token = auth_headers[1]
            data = jwt.decode(token, 'qwersdaiofjhoqwihlzxcjvjl')
            parse_name = data['sub']
            user = User.query.filter_by(username=parse_name).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            my_logger.error(e)
            return jsonify(invalid_msg), 401

    return _verify

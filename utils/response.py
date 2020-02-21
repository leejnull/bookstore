from django.http import JsonResponse
from .enums import StatusCode


def _response(status_code, message, data):
    response = JsonResponse({
        'status_code': status_code,
        'message': message,
        'data': data
    })
    response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Headers'] = 'Origin,X-Requested-With,Content-Type,Accept'
    response['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
    return response


def response_success(message='ok', data=None):
    return _response(StatusCode.SUCCESS, message, data)


def response_failure(status_code=StatusCode.BAD_REQUEST, message='failed', data=None):
    return _response(status_code, message, data)


def response_login():
    return _response(StatusCode.FAILED_AUTHORIZED, '未登录', None)

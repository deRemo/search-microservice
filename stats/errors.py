import functools

from flask import jsonify, request

'''
Constant value representing the endpoint. This has to be written with two
uppercase letter, eg. API Gateway -> AG)
'''
EP_CODE = 'SS'

'''
Dictionary with all errors related to this service and the
corresponding error messages and status_code
'''
EP_DICT = {
    # Auth errors
    '011': (400, 'You must provide a username'),
    '012': (400, 'You must provide a password'),
    '013': (400, 'You must provide an email'),
    '014': (400, 'Username or email already in use'),
    '021': (400, 'You must provide a username'),
    '022': (400, 'You must provide a password'),
    '023': (403, 'Invalid username or password'),
    '031': (401, 'You must provide an authentication token'),
    '032': (401, 'You must provide a valid authentication token'),

    # Users errors
    '111': (400, 'The identifier must be an integer'),
    '112': (404, 'You must provide an identifier associated to a registered user'),
    '121': (401, 'You must provide an authentication token'),
    '122': (401, 'You must provide a valid authentication token'),
    '131': (401, 'The identifier must be an integer'),
    '132': (404, 'You must provide an identifier associated to a registered user'),
    '133': (401, 'You must provide an authentication token'),
    '134': (401, 'You must provide a valid authentication token'),
    '135': (409, 'You are already following the requested user'),
    '141': (401, 'The identifier must be an integer'),
    '142': (404, 'You must provide an identifier associated to a registered user'),
    '143': (401, 'You must provide an authentication token'),
    '144': (401, 'You must provide a valid authentication token'),
    '145': (409, 'You are not following the requested user'),

    # Stats errors
    '411': (400, 'Error while saving statistics on the database'),
}


def response(code):
    '''
    Standard for the error response.

    The code must be written as a three number code, call it xyz, as follows:
        x -> the number of the current blueprint
        y -> the number of the route of the current blueprint
        z -> the number of the error within the current route

    Returns:
        A json response ready to be sent via a Flask view
    '''
    status_code, message = EP_DICT[code]
    return jsonify({
        'code': f'E{EP_CODE}{code}',
        'message': message
    }), status_code


def auth_required(error_code):
    '''
    Decorator for Flask view that requires an authentication token.

    Params:
        error_code -> The error code associated to this view

    Returns:
        If the token is not present then returns the error message associated
        to error_code, otherwise the normal return value of the wrapped
        function
    '''

    def _auth_required(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return response(error_code)
            return func(*args, **kwargs)

        return wrapper

    return _auth_required

# [Util - Src]

import jwt
import roundtop.config as config

from flask import jsonify, request
from datetime import datetime, timedelta
from roundtop import app

def check_table(funct:callable) -> callable:
    """
    Check Table <Wrapper>
    Will try to run passed in function until an attribute error is raised
    The attribute error indicates that the requested table does not exist
    If an AttributeError is raised then the function will simpy return {}
    
    @param funct <callable>: Function to be wrapped
    @returns <callable>: Wrapped function
    """

    def _wrap(*args, **kwargs) -> object:
        try:
            return funct(*args, **kwargs)
        except AttributeError:
            return jsonify({})
    _wrap.__name__ = funct.__name__
    
    return _wrap


def token_required(funct:callable) -> callable:
    """
    Token Required <Wrapper>
    Will require the use of a JWT in order to process request

    @param funct <callable>: Function to be wrapped
    @returns <callable>: Wrapped Function
    """

    def _wrap(*args, **kwargs):

        if not 'x-access-token' in request.headers: return jsonify({'message' : 'Token is missing !!'}), 401
        
        token = request.headers['x-access-token']
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")

        if data['auth'] != config.JWT_AUTH: 
            return jsonify({'message' : 'Token is invalid !!'}), 401
    
        return funct(*args, **kwargs)
    
    _wrap.__name__ = funct.__name__
    return _wrap

def make_token_response(**payload) -> object:
    """
    Make Token Response
    Used to generate a valid token response based on global environment data

    @param payload: key value pairs to be included in the JWT
    @returns : JWT
    """

    return jwt.encode(
        {'exp': datetime.utcnow() + timedelta(minutes=30), **payload}, 
        app.config['SECRET_KEY']
    )
        
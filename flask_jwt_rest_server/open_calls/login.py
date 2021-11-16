from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    password_from_user_form = request.form['password']
    print("form password is: ", password_from_user_form)
    user = {
            "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
            }
    username = request.form['firstname']
    print("form the user is: ", username)
    
    if not user:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    return json_response( token = create_token(user) , authenticated = True)


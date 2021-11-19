from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from tools.logging import logger

def handle_request():
    logger.debug("buy_book Handle Request")
    #use data here to auth the user

    username = request.form['username']
    print (username)   
  
    return json_response( status = "sucessful")      
    
       


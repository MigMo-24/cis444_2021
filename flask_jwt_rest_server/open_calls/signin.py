from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from tools.logging import logger

def handle_request():
    logger.debug("Signin Handle Request")
    #use data here to auth the user
    
     
    username = request.form['firstname']  
    password_from_user_form = request.form['password']
    print("form password is: ", password_from_user_form)
    print("form the user is: ", username) 

    salted = bcrypt.hashpw(bytes(password_from_user_form, 'utf-8'), bcrypt.gensalt(10))
    print(salted)
    cur = g.db.cursor()
    cur.execute(f"select * from _user where username = '{username}';")
    isFound = cur.fetchone()
    if isFound == None:
        salted = bcrypt.hashpw(bytes(password_from_user_form, 'utf-8'), bcrypt.gensalt(10))
        cur.execute("Insert into _user(username, password) values('%s','%s');" %(username,salted.decode('utf-8')))
        global_db_con.commit()
        user = {
            "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
            }
        return json_response( token = create_token(user) , authenticated = True)      
    
    
      return json_response(status_=401, message = 'Invalid credentials', authenticated =  False) )
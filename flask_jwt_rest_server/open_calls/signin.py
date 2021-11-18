from flask import request, g, render_template
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
        g.db.commit()
        sMessage = "User has been created, please logging"
        print(sMessage)
        return render_template('backatu.html', input_from_browser = sMessage,data = sMessage)
    else:
        print("existing user")
        str = (' Username exist');
        return json_response(data = str)

from flask import request, g, render_template
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    
     
    username = request.form['firstname']  
    password_from_user_form = request.form['password']
    print("form password is: ", password_from_user_form)
    print("form the user is: ", username) 
    salted = bcrypt.hashpw(bytes(password_from_user_form, 'utf-8'), bcrypt.gensalt(10))
    print(salted)
    cur=g.db.cursor()
    postgreSQL_select_Query =(f"select * from _user where username = %s ")
    cur.execute(postgreSQL_select_Query, (username,))
    username = cur.fetchone()[1]
    cur.execute(postgreSQL_select_Query, (username,))
    password = cur.fetchone()[2]
    print(username)                                                                                                            
    print(password)
    if (bcrypt.checkpw( bytes( password_from_user_form,'utf-8' ),password.encode('utf-8' ))):
        print("It matches")

        user = {
            "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
            }
        return json_response( token = create_token(user) , authenticated = True)      
    
    
    return render_template('backatu.html', input_from_browser = json_response(status_=401, message = 'Invalid credentials', authenticated =  False) )

from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
from tools.logging import logger

def handle_request():
    logger.debug("buy_book Handle Request")
    #use data here to auth the user
    book_id = form.request['book_id']
    print (book_id)   
    cur = g.db.cursor()
    cur.execute(f"select * from _book where book_id = '{book_id }';")
    found = cur.fetchall()
    cur.execute("Insert into purchase(found[0, found[1],found[2]) values('%s','%s','%s');" %(book_id, title, price))
    global_db_con.commit()
    
    return json_response( token = create_token(user) , authenticated = True)      
    
       


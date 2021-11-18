from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")   
    cur = g.db.cursor()
    cur.execute("Select * from _book")
    books = cur.fetchall()
    bookList = []
    for r in books:
        bookList.append(r)

    print("Books have ", books)
    return json_response( token = create_token(  g.jwt_data ), data = books)


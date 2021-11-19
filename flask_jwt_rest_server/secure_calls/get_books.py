from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")
    book_id = 0
    book_id = request.args.get('book_id')
    print(book_id)
    isEmpty = bool(book_id)
    print (isEmpty)
    if isEmpty == False :
       cur = g.db.cursor()
       cur.execute("Select * from _book")
       books = cur.fetchall()
       bookList = []
       for r in books:
           bookList.append(r)
           print("Books have ", books)
    else:
        cur = g.db.cursor()
        cur.execute(f"select * from _book where book_id = '{book_id}';")
        books = cur.fetchall()
        cur.execute(f"select * from _book where book_id = '{book_id}';") 
        bookName  = cur.fetchone()[1]
        cur.execute(f"select * from _book where book_id = '{book_id}';") 
        price = cur.fetchone()[3]
        print("The book selected is: ",bookName, price)
        cur.execute("Insert into purchase(title, price)values('%s', '%s');" %(bookName, price))
        g.db.commit()
        
    return json_response( token = create_token(  g.jwt_data ), data = books)


from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import datetime
import bcrypt


from db_con import get_db_instance, get_db
import datetime

app = Flask(__name__)


USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static/img",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "DEV"
JWT_SECRET = None

global_db_con = get_db()


with open("secret", "r") as f:
        JWT_SECRET = f.read()

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    return render_template('backatu.html',input_from_browser= str(request.form) )


#Assigment 2
@app.route('/ss1') #endpoint
def ss1():
    pagetitle = 'The HomePage'
    myparagraph = 'The professor is a good person, and he will give me and A.'
    return render_template('server_time.html',mytitle = pagetitle,mycontent =myparagraph ,server_time= str(datetime.datetime.now()) )

#Assigment 3

@app.route('/signup', methods=['POST'])#endpoint
def signup():
    username = request.form['username_signup_form']
    password = request.form['password_signup_form']
    cur = global_db_con.cursor()
    cur.execute(f"select * from _user where username = '{username}';")
    found = cur.fetchone()
    if found == None:
        salted = bcrypt.hashpw( bytes(username,  'utf-8' ) , bcrypt.gensalt(10))
        cur.execute("Insert into _user(username, password) values('%s','%s');" %(username,salted.decode('utf-8')))
        global_db_con.commit()
        jwt_str = jwt.encode({"username":username,"password":password}, JWT_SECRET, algorithm = "HS256")
        
        return json_response (data = jwt_str)
    else:
        print("Existing username")
        str = (' Username exist');
        return json_response(data = str)

@app.route('/logging', methods=['POST'])#endpoint
def logging():
    print(request.form)
    username = request.form['username_logging_form']
    password = request.form['password_logging_form']
    print("The username from the form: " + username)
    return json_response(password = password)
    salted = bcrypt.hashpw( bytes(password, 'utf-8') , bcrypt.gensalt(10))
    print(salted)
    print( str(salted.decode('utf-8')))
    cur=global_db_con.cursor()
    cur.execute(f"select * from users where username = '{username}';")
    userName = cur.fetchone()[1]
    cur.execute(f"select * from users where username = '{username}';")
    passWord = cur.fetchone()[2]
    print("The username from the database: " + userName)
    print("The password from the database: " + passWord)
    if (bcrypt.checkpw( bytes( password,'utf-8' ),passWord.encode('utf-8' ))):
        print("It matches")
        jwt_str = jwt.encode({"username":userName,"password":passWord}, JWT_SECRET, algorithm = "HS256")
        return json_response(data = jwt_str)
    else:
        print("It does not match:")
        msg=("mistmatch")
        return json_response(data = msg)

@app.route('/book', methods=['GET'])#endpoint
def books():
    cur = global_db_con.cursor()
    cur.execute("Select title from _book")
    book  =  cur.fetchall()
    print("Total rows are:  ", len(book))
    bookList = [] 
    for r in book:
        bookList.append(r)
        return json_response (data = book)

app.run(host='0.0.0.0', port=80)


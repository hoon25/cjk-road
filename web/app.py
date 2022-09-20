
from crypt import methods
import json
from flask import Flask, render_template, request, jsonify, flash, redirect, session

from web.common.mongo_connector import get_db, get_conn_with_collections
from web.common.response_factory import get_success_json, get_failure_json
from web.common.custom_logger import get_custom_logger

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.web

app = Flask(__name__)
app.secret_key = '111'

db = get_db()
logger = get_custom_logger("web")

@app.route('/')
def home():
    if "userID" in session:
        # print(session.get("userID"))
        # print("session ok")
        return render_template("index.html", email = session.get("userID"))
    else:
        # print("none session")
        return render_template("index.html")

@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")

@app.route('/login_action', methods=["GET"])
def login_action():
    email = request.args.get("email")
    password = request.args.get("password")
    user_info_db = db.web.find_one({"email" : email})

    if user_info_db is None:
        return redirect('/')
    else:
        db_email = user_info_db["email"]
        db_password = user_info_db["password"]
        if db_email == email and db_password == password:
            session["userID"] = email
            return redirect('/')
        else:
            return redirect('/login')
        
@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect('/')

# @app.route('/register_page', methods=['GET'])
@app.route('/signin', methods=['GET'])
def register_page():
    return render_template('signin.html')  


@app.route('/register', methods=['POST'])
def register():
    name = request.form["name"]
    nickname = request.form["nickname"]
    session['email'] = request.form["email"]
    session['password'] = request.form["password"]
    user_info = {"name": name, "nickname": nickname, "email": session['email'], "password": session['password']}
    db.web.insert_one(user_info)
    return redirect ("/")


@app.route('/user_list', methods=["GET"])
def user_list():
    # db.web.drop()
    user_list = list(db.web.find({}, {'_id': 0 }))
    return jsonify({'result':'success', 'msg':'Connected', 'data': user_list})


@app.route('/rest/<search_univ>', methods=['GET'])
def restaurant_get(search_univ):
    try:
        rest_list = list(db.restaurant.find({"university_name": search_univ}))
        for rest in rest_list:
            rest['_id'] = str(rest['_id'])
        result = get_success_json("검색 성공", rest_list)
        logger.info(result)
        return render_template('cards.html', result = result)

    except:
        flash("등록되지않은 대학교입니다.")
        return render_template('cards.html', result = get_failure_json("검색 실패"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
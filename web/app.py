from crypt import methods
import json
from flask import Flask, render_template, request, jsonify, redirect, session

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.web

app = Flask(__name__)
app.secret_key = '111'

# email1 = "jungle@gmail.com"
# password1 = "jungle"

@app.route('/')
def home():
    if "userID" in session:
        return render_template("index.html", email = session.get("userID"), login = True)
    else:
        return render_template("index.html", login = False)

@app.route('/login', methods=["GET"])
def login():
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
            return redirect('/')
        
@app.route("/logout")
def logout():
    session.pop("userID")
    return redirect('/')

@app.route('/register_page', methods=['GET'])
def register_page():
    return render_template('register_page.html')  


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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

 
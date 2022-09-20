from crypt import methods
import json
from flask import Flask, render_template, request, jsonify, redirect, session

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.web

app = Flask(__name__)
app.secret_key = '111'

email = "jungle@gmail.com"
password = "jungle"

@app.route('/')
def home():
    if "userID" in session:
        return render_template("index.html", email = session.get("userID"), login = True)
    else:
        return render_template("index.html", login = False)

@app.route('/login', methods=["GET"])
def login():
    global email, password
    email = request.args.get("email")
    password = request.args.get("password")
    
    if email == email and password == password:
        print(email, password)
        session["userID"] = email
        return redirect('/login')
    else:
        return redirect('/')
        

   
@app.route("/logout")
def logout():
    pass

@app.route('/register_page', methods=['GET'])
def register_page():
    return render_template('register_page.html')  


@app.route('/register', methods=['POST'])
def register():
    name = request.form["name"]
    nickname = request.form["nickname"]
    session['email'] = request.form["email"]
    session['password'] = request.form["password"]
    password_confrim = request.form["password_confirm"]
    user_info = {"name": name, "nickname": nickname, "email": session['email'], "password": session['password'], "password_confirm": password_confrim}
    db.web.insert_one(user_info)
    return redirect ("/")


@app.route('/user_list', methods=["GET"])
def user_list():
    user_list = list(db.web.find({}, {'_id': 0 }))
    return jsonify({'result':'success', 'msg':'Connected', 'data': user_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

 
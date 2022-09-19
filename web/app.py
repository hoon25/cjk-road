from crypt import methods
import json
from flask import Flask, render_template, request, jsonify

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.web

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/user_list', methods=["GET"])
def login():
    user_list = list(db.web.find({}, {'_id': 0 }))
    return jsonify({'result':'success', 'msg':'Connected', 'data': user_list})

@app.route('/register', methods=['POST'])
def register_api():
    name = request.form["name"]
    nickname = request.form["nickname"]
    email = request.form["email"]
    user_info = {"name": name, "nickname": nickname, "email": email}
    db.web.insert_one(user_info)
    return jsonify ({"result":"success"})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

 
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, render_template, request, jsonify, flash
# from web.common.mongo_connector import get_db, get_conn_with_collections
# from web.common.response_factory import get_success_json, get_failure_json
# from web.common.custom_logger import get_custom_logger
from common import mongo_connector, custom_logger, response_factory

app = Flask(__name__)

db = mongo_connector.get_db()
logger = custom_logger.get_custom_logger("web")

@app.route('/') 
def home():
   return render_template('login.html')

@app.route('/rest/<search_univ>', methods=['GET'])
def restaurant_get(search_univ):
    try:
        rest_list = list(db.restaurant.find({"university_name": search_univ}))
        for rest in rest_list:
            rest['_id'] = str(rest['_id'])
        result = response_factory.get_success_json("검색 성공", rest_list)
        logger.info(result)
        print(type(result['data']))
        return render_template('cards.html', restaurants = result['data'])

    except:
        flash("등록되지않은 대학교입니다.")
        return render_template('cards.html', result = response_factory.get_failure_json("검색 실패"))

if __name__ == '__main__':
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run('0.0.0.0', port=5500, debug=True)





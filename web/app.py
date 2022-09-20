from flask import Flask, render_template, request, jsonify, flash
from web.common.mongo_connector import get_db, get_conn_with_collections
from web.common.response_factory import get_success_json, get_failure_json
from web.common.custom_logger import get_custom_logger

app = Flask(__name__)

db = get_db()
logger = get_custom_logger("web")

@app.route('/')
def home():
   return render_template('login.html')

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
    app.run('0.0.0.0', port=5500, debug=True)




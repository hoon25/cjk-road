from pickle import NONE
import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, session, make_response
from bson.objectid import ObjectId
from common import mongo_connector, custom_logger, response_factory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, \
    decode_token

logger = custom_logger.get_custom_logger("web")

app = Flask(__name__)
JWT_SECRET_KEY = 'CJK-ROAD'
app.config.update(
    JWT_SECRET_KEY=JWT_SECRET_KEY
)

jwt = JWTManager(app)

db = mongo_connector.get_db()


@app.route('/')
def home():
    check_and_get_current_email(request)
    return render_template("index.html", email=check_and_get_current_email(request))


@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")


@app.route('/login_action', methods=["POST"])
def login_action():
    input_email = request.form["email"]
    input_password = request.form["password"]
    logger.info(f"INPUT: {input_email} {input_password}")
    user_info_db = db.user.find_one({"email": input_email})

    if user_info_db is None:
        return redirect('/')
    else:
        db_email = user_info_db["email"]
        db_password = user_info_db["password"]
        logger.info(f"DB: {db_email} {db_password}")
        if db_email == input_email and db_password == input_password:
            access_token = create_access_token(identity={"email": db_email},
                                               expires_delta=datetime.timedelta(minutes=120))
            logger.info(access_token)
            resp = make_response(redirect('/'))
            set_access_cookies(resp, access_token)

            return resp
        else:
            return redirect('/login')


@app.route("/logout")
def logout():
    resp = make_response(redirect('/'))
    unset_jwt_cookies(resp)
    return resp


@app.route('/signin', methods=['GET'])
def register_page():
    return render_template('signin.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form["name"]
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    user_info = {"name": name, "nickname": nickname, "email": email, "password": password}
    db.user.insert_one(user_info)
    return redirect("/")


@app.route('/user_list', methods=["GET"])
def user_list():
    user_list = list(db.user.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'msg': 'Connected', 'data': user_list})


@app.route('/rest/<search_univ>', methods=['GET'])
@jwt_required(['cookies'])
def restaurant_get(search_univ):
<<<<<<< HEAD
    rest_list = list(db.restaurant.find({"university_name": search_univ}))
    for rest in rest_list:
        rest['_id'] = str(rest['_id'])
    result = response_factory.get_success_json("검색 성공", rest_list)


    return render_template('cards.html', restaurants=result['data'], university=search_univ[:-2],
=======
    rest_list = get_rest_list(search_univ)

    return render_template('cards.html', restaurants=rest_list, university=search_univ[:-2],
>>>>>>> 863cb24a36273a9fed286923c8ebf8bbe65141d9
                           email=check_and_get_current_email(request))

def check_and_get_current_email(request):
    jwt_token = request.cookies.get('access_token_cookie')
    if jwt_token:
        current_user = decode_token(jwt_token)
        return current_user['sub']['email']
    return None

@app.route('/register/university', methods=['POST'])
def register_university():
    university = request.form['university_name']
    if (db.university.find_one({"university_name":university}) == None):
        db.university.insert_one({"university_name":university,"on":'N'})
    return redirect ("/university/list")

@app.route('/university/list')
def show_not_on_university():
    universities = list(db.university.find({'on':'N'},{'_id':False}))
    result = response_factory.get_success_json("검색 성공", universities)
    return render_template('university.html', universities=result['data'], email=check_and_get_current_email(request))


def get_rest_list(university_name):
    pipeline = [{'$match': {'university_name': university_name}},
{

        '$project': {
            '_id': {
                "$toString": "$_id"
            },
            'store_name': '$store_name',
            'store_star':'$store_star',
            'store_link':'$store_link',
            'store_pic':'$store_pic',
            'star_total': {
                '$ifNull': ['$star_total', 'null']
            }
        }
    },
        {
            '$lookup': {
                'from': 'restaurant_star',
                'localField': '_id',
                'foreignField': 'store_id',
                'as': 'star_total'
            }
        }]
    result = db.command('aggregate','restaurant', pipeline=pipeline, explain=False)
    rest_list = result['cursor']['firstBatch']
    for rest in rest_list:
        rest['_id'] = str(rest['_id'])
        sum = 0
        count = len(rest['star_total'])
        for star in rest['star_total']:
            sum += int(star['star'])
        if not sum == 0:
            avg = round(sum/count, 2)
        else:
            avg = 0
        rest['star_avg'] = avg
        rest['star_count'] = count
        del rest['star_total']
    return rest_list

@app.route('/rest/rate/<university>/<rest_id>', methods=['POST'])
def rate(university, rest_id):
    email = check_and_get_current_email(request)
    
    # restaurant_star 컬랙션에 필요한 정보 수집
    restaurant_id = rest_id
    star = int(request.form["rate-radio"][-1])
    rateing_info = {'restaurant_id': restaurant_id, 'star': star, "user_email" : email}

    # db넣기
    db.restaurant_star.insert_one(rateing_info)

    # db에서 평균을 구할 가게 id 같은거 전부 추출 후 평균 계산
    target_store_list = (list(db.restaurant_star.find({"store_id": restaurant_id})))
    sum_star = 0
    for target_store in target_store_list:
        sum_star = sum_star + target_store["star"]
    sum_person_number= len(target_store_list)
    star_average= round(sum_star/sum_person_number,1) 

    # 수정해야함!
    return render_template('index.html', star_average = star_average, sum_person_number= sum_person_number)
    # return render_template(f'/rest/{university}', star_average = star_average, sum_person_number= sum_person_number)
    # return redirect (f'/rest/{university}', star_average = star_average, sum_person_number= sum_person_number)
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5500, debug=True)

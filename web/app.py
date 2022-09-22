import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, session, make_response
from common import mongo_connector, custom_logger, response_factory
from batch.service import restaurant_crawl_service
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, \
    decode_token

logger = custom_logger.get_custom_logger("web")

app = Flask(__name__)
JWT_SECRET_KEY = 'CJK-ROAD'
app.config.update(
    JWT_SECRET_KEY=JWT_SECRET_KEY
)
app.secret_key = "HI"

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
        flash("로그인에 실패하셨습니다.")
        return redirect('/login')
    else:
        db_email = user_info_db["email"]
        db_password = user_info_db["password"]
        db_role = user_info_db['role']
        logger.info(f"DB: {db_email} {db_password}")
        if db_email == input_email and db_password == input_password:
            access_token = create_access_token(identity={"email": db_email, "role": db_role},
                                               expires_delta=datetime.timedelta(minutes=120))

            flash("로그인에 성공하셨습니다.")
            logger.info(access_token)
            resp = make_response(redirect('/'))
            set_access_cookies(resp, access_token)

            return resp
        else:
            flash("로그인에 실패하셨습니다.")
            return redirect('/login')


@app.route("/logout")
def logout():
    resp = make_response(redirect('/'))
    unset_jwt_cookies(resp)
    return resp


@app.route('/signin', methods=['GET'])
def register_page():
    return render_template('signin.html')


def valid_signin_exists_email(email):
    user_count = list(db.user.find({'email': email}))
    if len(user_count) != 0:
        flash("이미 존재하는 ID입니다.")
        return False
    return True


@app.route('/register', methods=['POST'])
def register():

    name = request.form["name"]
    nickname = request.form["nickname"]
    email = request.form["email"]
    password = request.form["password"]
    role = "USER"

    if not valid_signin_exists_email(email):
        return redirect("/")

    user_info = {"name": name, "nickname": nickname, "email": email, "password": password, "role": role}
    db.user.insert_one(user_info)

    return redirect("/")


@app.route('/user_list', methods=["GET"])
def user_list():
    user_list = list(db.user.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'msg': 'Connected', 'data': user_list})


@app.route('/rest/<search_univ>', methods=['GET'])
def restaurant_get(search_univ):
    rest_list = get_rest_list(search_univ)

    return render_template('cards.html', restaurants=rest_list, university=search_univ[:-2],
                           email=check_and_get_current_email(request))


def check_and_get_current_email(request):
    jwt_token = request.cookies.get('access_token_cookie')
    if jwt_token:
        current_user = decode_token(jwt_token)
        return current_user['sub']['email']
    return None

def check_admin(request):
    jwt_token = request.cookies.get('access_token_cookie')
    if jwt_token:
        current_user = decode_token(jwt_token)
        print(current_user['sub']['role'])
        if current_user['sub']['role'] == 'ADMIN':
            flash("등록완료되었습니다.")
            return True
    flash("관리자만 접근 가능합니다.")
    return False


@app.route('/register/university', methods=['POST'])
def register_university():
    university = request.form['university_name']
    if (db.university.find_one({"university_name": university}) == None):
        db.university.insert_one(
            {"university_name": university, "on": 'N', 'created_by': check_and_get_current_email(request)})
    return redirect("/university/list")


@app.route('/university/list')
def show_not_on_university():
    universities_y = list(db.university.find({'on': 'Y'}, {'_id': False}))
    universities_n = list(db.university.find({'on': 'N'}, {'_id': False}))
    return render_template('university.html', universities_y=universities_y, universities_n=universities_n,
                           email=check_and_get_current_email(request))


def get_rest_list(university_name):
    pipeline = [{'$match': {'university_name': university_name}},
                {

                    '$project': {
                        '_id': {
                            "$toString": "$_id"
                        },
                        'university_name': '$university_name',
                        'store_name': '$store_name',
                        'store_star': '$store_star',
                        'store_link': '$store_link',
                        'store_pic': '$store_pic',
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
    result = db.command('aggregate', 'restaurant', pipeline=pipeline, explain=False)
    rest_list = result['cursor']['firstBatch']
    for rest in rest_list:
        rest['_id'] = str(rest['_id'])
        sum = 0
        count = len(rest['star_total'])
        for star in rest['star_total']:
            sum += int(star['star'])
        if not sum == 0:
            avg = round(sum / count, 2)
        else:
            avg = 0
        rest['star_avg'] = avg
        rest['star_count'] = count
        del rest['star_total']
    return rest_list


def valid_user_click_star(store_id, email):
    if not email:
        flash("로그인이 필요합니다.")
        return False

    user_count = list(db.restaurant_star.find({'store_id': store_id, 'user_email': email}))
    if len(user_count) != 0:
        flash("이미 평점을 등록한 맛집입니다.")
        return False

    return True


@app.route('/rest/rate/<university>/<rest_id>', methods=['POST'])
def rate(university, rest_id):
    try:
        email = check_and_get_current_email(request)
        if not valid_user_click_star(str(rest_id), email):
            return redirect(f'/rest/{university}')

        # restaurant_star 컬랙션에 필요한 정보 수집
        restaurant_id = rest_id
        star = int(request.form["rate-radio"][-1])
        rating_info = {'store_id': restaurant_id, 'star': star, "user_email": email}

        # db넣기
        db.restaurant_star.insert_one(rating_info)

    except:
        logger.exception("별점 등록 에러")
    return redirect(f'/rest/{university}')


@app.route('/<university_name>/save', methods=['GET'])
def save_university(university_name):
    if check_admin(request):
        restaurant_crawl_service.main([university_name+'맛집'])
        db.university.update_one({'university_name': university_name},
                                 {'$set': {'on': 'Y'}})
    return redirect('/university/list')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5500, debug=True)

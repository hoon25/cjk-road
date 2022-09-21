from batch.common.mongoConnector import get_conn
import math
#
# restaurant_star = get_conn('restaurant_star')
# restaurant = get_conn('restaurant')
#
# star_list = restaurant_star.find({'store_name': '연교'})
# print(star_list)
#
# rest_star_list = []
# for star in star_list:
#     rest_star_list.append(star['star'])
#
# print(sum(rest_star_list)/len(rest_star_list))
# rest_avg = sum(rest_star_list)/len(rest_star_list)
#
# rest_one = restaurant.find_one({'store_name':'연교'})
# print(rest_one)
#
# rest_one['rest_avg'] = rest_avg
#
# print("반환값")
# print(rest_one)



from common import mongo_connector
db = mongo_connector.get_db()


def get_star_avg_and_count(university_name):
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



get_star_avg_and_count('고려대학교맛집')
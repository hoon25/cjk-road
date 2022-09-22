import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parent.parent.parent.as_posix())
from batch.common.mongoConnector import save_data, get_conn
from batch.N_Map_Crawling import restaurant_crawling
import time


def main(univ_list):
    for univ in univ_list:
        data = restaurant_crawling.main(univ)
        save_data("restaurant", data)
        time.sleep(1)

if __name__ == "__main__":
    # 스크립트 수동 실행 시 전체 데이터 적재
    db = get_conn()
    univ_list = db.university.find({'on': 'Y'})
    keyword_list = []
    for univ in univ_list:
        keyword_list.append(univ['university_name'] + "맛집")
    main(keyword_list)
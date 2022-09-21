from batch.common.mongoConnector import save_data
from batch.N_Map_Crawling import restaurant_crawling
import sys


def main():
    univ_list = ["서울대학교맛집", "고려대학교맛집", "연세대학교맛집"]
    keyword = "연세대학교맛집"
    data = restaurant_crawling.main(keyword)
    save_data("restaurant", data)


if __name__ == "__main__":
    main()

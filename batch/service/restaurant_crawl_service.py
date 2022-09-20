from batch.common.mongoConnector import save_data
from batch.N_Map_Crawling import restaurant_crawling
import sys

def main():
    data = restaurant_crawling.main("연세대학교맛집")
    save_data("restaurant", data)


if __name__ == "__main__":
    main()
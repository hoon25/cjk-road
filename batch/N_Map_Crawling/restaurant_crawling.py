import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parent.parent.parent.as_posix())
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib import parse
from batch.common.custom_logger import get_custom_logger
import re

logger = get_custom_logger("crawl")

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
# options.add_argument('--disable-gpu')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")

# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()

def main(key_word):
    try:
        start_time = time.time()
        url = "https://map.naver.com/v5/search"
        logger.info(f"검색 키워드 : {key_word}")
        driver.get(url)
        time_wait(10, 'div.input_box > input.input_search')

        search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
        search.send_keys(key_word)
        search.send_keys(Keys.ENTER)

        time.sleep(1)
        switch_frame('searchIframe')
        time.sleep(1)
        page_down(40)
        time.sleep(1)

        # 매장 리스트
        store_master = driver.find_elements(By.CSS_SELECTOR, 'div.Ryr1F > ul > li')
        store_dict_list = []

        logger.info(f"결과 개수  : {len(store_master)}건")

        for store in store_master:
            logger.debug("---------------------------------------------------")
            store_name, store_star, store_link = '', '', ''
            store_dict = {}
            logger.debug("---------------------이름")
            store_name = store.find_element(By.CSS_SELECTOR, 'div.CHC5F > a > div > div > span.place_bluelink.TYaxT').text
            logger.debug(store_name)
            logger.debug("---------------------별점")
            try:
                store_star = store.find_element(By.CSS_SELECTOR, 'div.CHC5F > div.Dr_06 > span.h69bs.a2RFq > em').text
            except:
                store_star = "0.0"
            logger.debug(store_star)
            logger.debug("---------------------링크")
            store_link = f"https://map.naver.com/v5/search/{parse.quote(store_name)}/"
            logger.debug(store_link)
            try:
                logger.debug("---------------------사진")
                store_pic_list = store.find_elements(By.CSS_SELECTOR, 'div.N_3Z8 > div > a > div > div')
                store_pic_all = store_pic_list[0]
                store_pic_string = store_pic_all.get_attribute('style')
                m = re.search('url\("(.*?)"\)', store_pic_string)
                store_pic = m.group(1)
                logger.debug(store_pic)
            except:
                store_pic = "N"

            store_dict = {'university_name': key_word, 'store_name': store_name, 'store_star': store_star, 'store_link': store_link, 'store_pic': store_pic}
            store_dict_list.append(store_dict)
        return store_dict_list
    except:
        logger.exception(f"{key_word} 크롤링 실패")
    finally:
        # driver.quit()
        logger.info(f"소요시간:{time.time() - start_time}")
        time.sleep(2)


# 페이지 로드 대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        logger.exception(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait


# 프레임 변경
def switch_frame(frame):
    driver.switch_to.default_content()
    driver.switch_to.frame(frame)


# 페이지 내리기
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    # driver.execute_script("console.log(document.querySelectorAll('body'))")
    # driver.execute_script("document.querySelector('body').click()")
    # driver.execute_script("document.getElementsByClassName('Fufu_')[0].click()")
    # driver.execute_script("window.scrollTo(0,100)")

    # driver.execute_script("console.log(document.getElementById('searchIframe').contentWindow)")
    # driver.execute_script("console.log(document.getElementById('searchIframe').body.scrollHeight)")
    # driver.execute_script("document.getElementById('searchIframe').contentWindow.scrollTo(0, 100000);")

    # for i in range(num):
    #     # driver.execute_script("myIframe.contentWindow.scrollTo(0, document.body.scrollHeight);")
    #     driver.execute_script("document.getElementById('searchIframe').contentWindow.scrollTo(0, 100000);")

    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)


# 메인 함수
if __name__ == "__main__":
    key_word = sys.argv[1]
    main(key_word)


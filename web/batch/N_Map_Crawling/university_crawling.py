from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib import parse
from batch.common.custom_logger import get_custom_logger
import sys

logger = get_custom_logger("crawl")
driver = webdriver.Chrome()


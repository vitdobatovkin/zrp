# открытие ADS
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

#логгер
from loguru import logger


class AdsProfile:
    def __init__(self, ads_id):
        self.ads_id = ads_id
        self.driver = None

    def start(self):
        open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + self.ads_id

        resp = requests.get(open_url).json()
        if resp["code"] != 0:
            logger.error(f'Failed to start {self.ads_id}')
            return

        chrome_driver = resp["data"]["webdriver"]
        service = Service(executable_path=chrome_driver)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info(f'{self.ads_id} has been started')



    def stop(self):
        close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + self.ads_id
        resp = requests.get(close_url).json()

        if resp['code'] != 0:
            logger.error(f'Failed to stop {self.ads_id}')
            return
        else:
            logger.info(f'{self.ads_id} has been stopped')
import logging

import requests
from requests.exceptions import *
from selenium import webdriver

from tqdm import tqdm


class Visitor(object):

    def __init__(self, url, logger=None):
        self.__url = url
        self.logger = logger or logging.getLogger(__name__)
        self.req = requests
        #self.__driver = webdriver.Chrome()

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    def visitNoUI(self, count=1, timeout=0.1):
        try:
            for i in tqdm(range(count)):
                try:
                    self.req.get(self.url, timeout=timeout)
                except MissingSchema as err:
                    self.logger.err(err)
                    raise RuntimeError("Invalid URL")
                except ConnectionError as err:
                    self.logger.info(err)
        except Exception as err:
            self.logger.error(err, exc_info=True)

import logging

import requests
from requests.exceptions import *
from selenium import webdriver

from modules.tqdm import tqdm


class Visitor(object):

    def __init__(self, url, logger=None):
        self.__url = url
        self.logger = logger or logging.getLogger(__name__)
        self.req = requests
        self.__timeout = 1
        self.__readCount = 0
        #self.__driver = webdriver.Chrome()

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if value != self.url:
            self.logger.debug("url changed to %s" % (value))
            self.__readCount = 0
            self.__timeout = 1
        self.__url = value

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        self.logger.debug("timeout changed to %d" % (int(value)))
        self.__timeout = value

    @property
    def validVisits(self):
        return int(self.__readCount)

    @validVisits.setter
    def validVisits(self, value):
        self.__readCount = value

    def visitNoUI(self, count=1, timeout=None, selfHeal=None):
        if timeout is not None:
            self.timeout = timeout
        try:
            for i in tqdm(range(count)):
                try:
                    self.req.get(self.url, timeout=self.timeout)
                    self.validVisits = self.validVisits + 1
                except MissingSchema as err:
                    self.logger.err(err)
                    raise RuntimeError("Invalid URL")
                except ConnectionError as err:
                    self.logger.debug(err)
                except ReadTimeoutError as err:
                    self.logger.debug(err)
                    self.timeout = self.timeout + 1
                except ConnectTimeoutError as err:
                    self.logger.debug(err)
                    self.timeout = self.timeout + 1
            if selfHeal and self.validVisits != count:
                self.visitNoUI(count=(count - self.validVisits), timeout=self.timeout, selfHeal=False)
            self.logger.info("visited %s \t {%d} times" % (str(self.url), int(self.validVisits)))
            return self.validVisits
        except Exception as err:
            self.logger.error(err, exc_info=True)
            return self.validVisits

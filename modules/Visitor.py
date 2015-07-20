import logging
import socket
import urllib

import requests
from requests.exceptions import *
from selenium import webdriver

import socks
from modules.tqdm import tqdm
from sockshandler import SocksiPyHandler


class Visitor(object):

    def __init__(self, url, logger=None):
        self.__url = url
        self.logger = logger or logging.getLogger(__name__)
        self.req = requests
        self.__timeout = 1
        self.__readCount = 0
        self.__tor = urllib.request.build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150))
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
    def torBrowser(self):
        return self.__tor

    @property
    def validVisits(self):
        return int(self.__readCount)

    @validVisits.setter
    def validVisits(self, value):
        self.__readCount = value

    def visitNoUI(self, count=1, timeout=None, selfHeal=None, use_tor=None):
        if timeout is not None:
            self.timeout = timeout
        try:
            for i in tqdm(range(count)):
                if use_tor:
                    try:
                        socket.setdefaulttimeout(self.timeout)
                        self.torBrowser.open(self.url)
                        self.validVisits = self.validVisits + 1
                        if self.timeout > 5:
                            self.timeout = self.timeout -1
                    except socks.GeneralProxyError:
                        self.logger.error("TOR Proxy is Down")
                        raise RuntimeError
                    except socket.timeout as err:
                        self.logger.debug(err)
                        self.timeout = self.timeout + 1
                    except ValueError as err:
                        self.logger.error(err)
                        raise RuntimeError("Invalid URL")
                    except urllib.error.URLError as err:
                        self.logger.debug(err)
                        self.timeout = self.timeout + 1
                else:
                    try:
                        self.req.get(self.url, timeout=self.timeout)
                        self.validVisits = self.validVisits + 1
                    except MissingSchema as err:
                        self.logger.error(err)
                        raise RuntimeError("Invalid URL")
                    except ConnectionError as err:
                        self.logger.debug(err)
                    except ReadTimeout as err:
                        self.logger.debug(err)
                        self.timeout = self.timeout + 1
                    except ConnectTimeoutError as err:
                        self.logger.debug(err)
                        self.timeout = self.timeout + 1
            if selfHeal and self.validVisits != count:
                self.visitNoUI(count=(count - self.validVisits), timeout=self.timeout, selfHeal=True, use_tor=use_tor)
            self.logger.info("visited %s \t {%d} times" % (str(self.url), int(self.validVisits)))
            return self.validVisits
        except Exception as err:
            self.logger.error(err, exc_info=True)
            return self.validVisits

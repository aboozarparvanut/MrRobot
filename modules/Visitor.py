import csv
import logging
import re
import socket
import urllib

import requests
from requests.exceptions import *
from selenium import webdriver

import socks
from bs4 import BeautifulSoup
from modules.Parser import Parser
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
        # default browser is chrome 41 on windows 8
        self.__env = Parser(self.logger, "../conf/browsers.ini")
        self.__headers = {'user-agent': self.env.getConfig("Chrome", env="Windows")}
        #self.__driver = webdriver.Chrome()

    @property
    def env(self):
        return self.__env

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
    def header(self):
        return self.__headers

    @property
    def validVisits(self):
        return int(self.__readCount)

    @validVisits.setter
    def validVisits(self, value):
        self.__readCount = value

    def visitNoUI(self, count=None, timeout=None, selfHeal=None, use_tor=None, round=None):
        if timeout is not None:
            self.timeout = timeout
        if count is None:
            count = 1
        try:
            for i in tqdm(range(count)):
                if use_tor:
                    try:
                        socket.setdefaulttimeout(self.timeout)
                        self.torBrowser.open(self.url)
                        self.validVisits = self.validVisits + 1
                        if self.timeout > 5:
                            self.timeout = self.timeout - 1
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
                        #s = self.req.Session()
                        r = self.req.get(str(self.url), timeout=self.timeout, headers=self.header)
                        self.validVisits = self.validVisits + 1
                        if self.validVisits == 1:
                            self.parseEmail(r.text)
                    except MissingSchema as err:
                        self.logger.exception(err)
                        raise RuntimeError("Invalid URL")
                    except ConnectionError as err:
                        self.logger.debug(err)
                    except ReadTimeout as err:
                        self.logger.debug(err)
                        self.timeout = self.timeout + 1
                    # except ConnectTimeoutError as err:
                    #    self.logger.debug(err)
                    #    self.timeout = self.timeout + 1
            if selfHeal and self.validVisits != count:
                if round is None:
                    round = 1
                if round == 3:
                    self.visitNoUI(count=(count - self.validVisits), timeout=self.timeout,
                                   selfHeal=False, use_tor=use_tor, round=round + 1)
                else:
                    self.visitNoUI(count=(count - self.validVisits), timeout=self.timeout,
                                   selfHeal=True, use_tor=use_tor, round=round + 1)
            self.logger.info("visited %s \t {%d} times" % (str(self.url), int(self.validVisits)))
            return self.validVisits
        except Exception as err:
            self.logger.exception(err)
            return self.validVisits

    def parseEmail(self, file):

        # convert the infile to soup object
        soup = BeautifulSoup(file, "html.parser")

        # find all mailto (email) elements
        mailtos = soup.select('a[href^=mailto]')

        emails = []

        # Extract emails
        for i in mailtos:
            if i.string != None:
                emails.append(str(i.string.encode('utf-8').strip().decode(encoding="utf-8")))
        # Store to File
        try:
            pars = Parser(self.logger, "../conf/application.ini")
            outFile = pars.getConfig("emails", env="production")
            with open(outFile, 'a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(emails)
                return emails
        except Exception as err:
            self.logger.exception(err)
            return None

import configparser
import os


class Parser(object):

    def __init__(self, logger):
        self.__config = configparser.ConfigParser()
        APPLICATION_CONF = os.path.join(os.path.dirname(__file__),
                                        "../conf/browsers.ini")
        self.logger = logger
        self.__config.read(APPLICATION_CONF)
        self.__environment = self.ConfigSectionMap("Default")['env']

    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, value):
        self.__environment = value

    def getConfig(self, value, env=None):
        if env is None:
            env = self.environment
        try:
            result = self.ConfigSectionMap(env)[str(value).lower()]
            return result
        except Exception as err:
            self.logger.debug(err)
            return None

    def ConfigSectionMap(self, section):
        try:
            dict1 = {}
            options = self.__config.options(section)
            for option in options:
                try:
                    dict1[option] = self.__config.get(section, option)
                except Exception as err:
                    self.logger.debug(err)
                    dict1[option] = None
            return dict1
        except configparser.NoSectionError as err:
            self.logger.debug(err)
            return None

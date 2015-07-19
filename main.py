import logging
import logging.config

from modules.Visitor import Visitor


def main():
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger()
    url = input("please enter URL:")
    visit = Visitor(url=url, logger=logger)
    visit.visitNoUI(count=20, timeout=1)

if __name__ == "__main__":
    main()

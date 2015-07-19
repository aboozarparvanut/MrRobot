import logging
import logging.config

from modules.Visitor import Visitor


def main():

    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger()
    try:
        url = input("please enter URL:")
        count = int(input("please enter number of visits:"))
        robot = Visitor(url=url, logger=logger)
        vistedTimes = robot.visitNoUI(count=count, timeout=1)
        print("you've asked %d times and i've visited %d times" % (count, robot.validVisits))
    except Exception as err:
        logger.error(err)

if __name__ == "__main__":
    main()

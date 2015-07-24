import logging
import logging.config

from modules.Visitor import Visitor


def main():

    logging.config.fileConfig('conf/logging.ini')
    logger = logging.getLogger()
    while True:
        try:
            use_tor = input("Do you want to use MultiIP capability[N]?: ")
            if use_tor.lower() in ['y', 'yes']:
                use_tor = True
            else:
                use_tor = False
            url = input("please enter URL:")
            countRaw = input("please enter number of visits:")
            if countRaw.isnumeric():
                count = int(countRaw)
            else:
                count = 1
            robot = Visitor(url=url, logger=logger)
            vistedTimes = robot.visitNoUI(count=count, timeout=1, selfHeal=True, use_tor=use_tor)
            print("you've asked %d times and ive visited %d times" % (count, robot.validVisits))
            result = input("do you want to visit another site[N]")
            if result.lower() != 'y':
                print("bye bye...")
                break
        except KeyboardInterrupt as err:
            answer = input("Are you sure you want to exit the program?[Y]")
            if answer is None:
                print("Sayonara...")
                break
            if answer.lower in ['n', 'no']:
                continue
            else:
                print("Farewell...")
                break
        except Exception as err:
            logger.error(err)
            continue


if __name__ == "__main__":
    main()

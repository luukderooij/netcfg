from commands.ping import Pinger
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    pinger = Pinger(host="8.8.8.8", infinite=False, count=5)

    for line in pinger.run():
        # In GUI kun je deze 'line' direct doorsturen naar een tekstvak
        print(line)
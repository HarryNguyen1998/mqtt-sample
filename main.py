import logging
import signal
import time

from pub import Publisher

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(name)s: %(message)s")

BROKER_ADDR = "emqx_broker"

logger = logging.getLogger()

RUNNING = True


def shutdown_script(*args):
    logger.info("Exiting...")
    global RUNNING
    RUNNING = False


def main():
    signal.signal(signal.SIGINT, shutdown_script)
    signal.signal(signal.SIGTERM, shutdown_script)

    logger.info("Starting...")
    publisher = Publisher(BROKER_ADDR)
    publisher.topic = "charger/1/connector/1/session/1"
    publisher.connect()

    while RUNNING:
        time.sleep(1)


if __name__ == "__main__":
    main()

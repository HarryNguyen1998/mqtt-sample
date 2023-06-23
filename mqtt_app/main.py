import logging
import os
import signal
import threading

from publisher.content_generator import generate_content
from publisher.publisher import Publisher

logging.basicConfig(
    level=logging.DEBUG, format="%(thread)d [%(threadName)s] %(levelname)-6s %(name)s: %(message)s"
)
logger = logging.getLogger()


def register_cleanup(pub: Publisher, exit_flag: threading.Event):
    def cleanup(signalnum, handler):
        pub.disconnect()
        exit_flag.set()
        logger.info("Goodbye")

    # Handles Ctrl-C when running from local.
    signal.signal(signal.SIGINT, cleanup)
    # Handles SIGTERM when running from container.
    signal.signal(signal.SIGTERM, cleanup)


def main():
    # Initialize
    exit_flag = threading.Event()
    pub = Publisher(os.environ.get("BROKER_ADDR", "MSI.local"))
    pub.connect()
    register_cleanup(pub, exit_flag)

    # Run the main loop.
    logger.info("Running...")
    while not exit_flag.is_set():
        exit_flag.wait(15)


if __name__ == "__main__":
    main()

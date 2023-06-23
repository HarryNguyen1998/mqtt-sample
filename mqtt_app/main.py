import logging
import sys
import os
import signal
import threading

from model.content_generator import generate_content
from infra.publisher import Publisher

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s"
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
    # Initialize.
    exit_flag = threading.Event()
    pub = Publisher(os.environ.get("BROKER_ADDR", "mqtt_broker"))

    # Connection.
    try: 
        pub.connect()
    except Exception as ex:
        logger.error(f"Failed to connect, ex={ex}")
        sys.exit(1)

    # Waiting for connection before publishing.
    while not pub.connected:
        exit_flag.wait(1)

    if pub.bad_connect:
        sys.exit(1)

    register_cleanup(pub, exit_flag)

    # Main loop.
    logger.info("Running...")
    while not exit_flag.is_set():
        logger.info("Publishing...")
        topic, content = generate_content()
        pub.topic = topic
        pub.publish(content, 2)
        exit_flag.wait(5)


if __name__ == "__main__":
    main()

import logging
import os
import signal
import sys
import threading

from mqtt_app.models.content_generator import generate_content
from mqtt_app.transport import Publisher, Subscriber

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s"
)
logger = logging.getLogger()


def register_cleanup(pub: Publisher, sub: Subscriber, exit_flag: threading.Event):
    def cleanup(signalnum, handler):
        exit_flag.set()
        pub.disconnect()
        sub.disconnect()
        logger.info("Goodbye")

    # Handles Ctrl-C when running from local.
    signal.signal(signal.SIGINT, cleanup)
    # Handles SIGTERM when running from container.
    signal.signal(signal.SIGTERM, cleanup)


def main():
    # Initialize.
    exit_flag = threading.Event()
    pub = Publisher(os.environ.get("BROKER_ADDR", "mqtt_broker"))
    sub = Subscriber(os.environ.get("BROKER_ADDR", "mqtt_broker"))
    register_cleanup(pub, sub, exit_flag)

    # Connection.
    try:
        pub.connect()
        sub.connect()
    except Exception as ex:
        logger.error(f"Failed to connect, ex={ex}")
        sys.exit(1)

    # Waiting for connection before publishing. The exit_flag is present since
    # signal could be raised while connection is in progress.
    while (
        (not pub.connected or pub.bad_connect)
        and (not pub.connected or pub.bad_connect)
        and not exit_flag.is_set()
    ):
        exit_flag.wait(1)

    if pub.bad_connect or sub.bad_connect:
        sys.exit(1)

    # Main loop.
    sub.subscribe("charger/1/connector/1/session/1")
    logger.info("Running...")
    while not exit_flag.is_set():
        logger.info("Publishing...")
        topic, content = generate_content()
        pub.topic = topic
        pub.publish(content, 2)
        exit_flag.wait(10)


if __name__ == "__main__":
    main()

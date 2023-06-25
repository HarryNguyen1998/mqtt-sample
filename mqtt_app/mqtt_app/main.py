import logging
import signal
import sys
import threading
from typing import Callable

from mqtt_app.config import Config
from mqtt_app.models.content_generator import charger_sessions_gen
from mqtt_app.transport import Publisher, Subscriber

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s"
)
logger = logging.getLogger()


def register_exit_signal_handler(shutdown: Callable[[], None]):
    """Register callback to be called when receiving SIGINT or SIGTERM."""
    def cleanup(signalnum, handler):
        shutdown()

    # Handles Ctrl-C when running from local.
    signal.signal(signal.SIGINT, cleanup)
    # Handles SIGTERM when running from container.
    signal.signal(signal.SIGTERM, cleanup)


def main():
    # Initialize.
    exit_flag = threading.Event()
    pub = Publisher(Config.BROKER_ADDR, debug=Config.DEBUG_PRINT)
    sub = Subscriber(Config.BROKER_ADDR, debug=Config.DEBUG_PRINT)
    generator_instance = charger_sessions_gen()

    def shutdown():
        pub.disconnect()
        sub.disconnect()
        exit_flag.set()
        logger.info("Goodbye")

    register_exit_signal_handler(shutdown)

    # Setup connection.
    try:
        pub.connect()
        sub.connect()
    except Exception as ex:
        logger.error(f"Abort because setup is wrong, ex={ex}")
        sys.exit(1)

    # Waiting loop.
    while not exit_flag.is_set():
        if pub.connected and sub.connected:
            break

        if pub.bad_connected or sub.bad_connected:
            logger.error("Abort because connection was refused.")
            shutdown()

        exit_flag.wait(1)

    # Main loop.
    subscribe_topic = "charger/1/connector/1/session/+"
    try:
        sub.subscribe(subscribe_topic)
    except Exception as ex:
        logger.error(f"Abort because failed to subscribe ex={ex}")
        shutdown()

    while not exit_flag.is_set():
        # Make sure the subscriber is connected, so that message can be received
        # for the 1st time.
        if not sub.acknowledged(subscribe_topic):
            exit_flag.wait(1)
            continue

        topic, content = next(generator_instance)
        pub.topic = topic
        pub.publish(content)
        exit_flag.wait(60)


if __name__ == "__main__":
    main()

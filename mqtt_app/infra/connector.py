import abc
import logging
import os
import threading

import paho.mqtt.client as mqttc

logger = logging.getLogger(__name__)


class MQTTConnector(abc.ABC):
    """A connector that handles connection to a MQTT broker."""

    def __init__(self, broker_addr, name="", debug=False):
        self._broker_addr = broker_addr
        self._connected = False
        self._bad_connect = False
        self._disconnect_flag = threading.Event()

        self.client = mqttc.Client(name)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        if os.environ.get("APP_DEBUG"):
            self.client.enable_logger(logger)

    def connect(self):
        """Set up connection to the MQTT broker."""
        logger.info(f"Connecting to {self._broker_addr}...")
        self.client.connect(self._broker_addr)
        self.client.loop_start()

    def disconnect(self):
        """Closes connection to the MQTT broker."""
        logger.info(f"Disconnecting from {self._broker_addr}...")
        self.client.disconnect()

        # Only wait for the disconnect if already connected.
        if self._connected:
            self._disconnect_flag.wait(5)

    @property
    def connected(self):
        return self._connected

    @property
    def bad_connect(self):
        return self._bad_connect

    def on_connect(self, client, userdata, flags, conn_rc):
        self._connected = True
        if conn_rc == 0:
            logger.info("MQTT connection established")
        else:
            self._bad_connect = True
            logger.error(f"MQTT connection failed, rc={conn_rc}")

    def on_disconnect(self, client, userdata, conn_rc):
        if conn_rc == 0:
            self.client.loop_stop()
            self._disconnect_flag.set()
            logger.info("Disconnect successfully")
        else:
            logger.error(f"Unexpected disconnect, rc={conn_rc}")

        self._connected = False

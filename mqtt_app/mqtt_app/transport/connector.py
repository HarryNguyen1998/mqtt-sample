import abc
import logging
import threading

import paho.mqtt.client as mqttc


class MQTTConnector(abc.ABC):
    """A connector that handles connection to a MQTT broker."""

    def __init__(self, broker_addr, name="", debug=False):
        self._broker_addr = broker_addr
        self._connected = False
        self._bad_connected = False
        self._disconnect_flag = threading.Event()
        self.log = logging.getLogger(self.__class__.__name__)

        self.client = mqttc.Client(name)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        if debug:
            self.client.enable_logger(self.log)

    def connect(self):
        """Set up connection to the MQTT broker."""
        self.log.info("Connection process started.")
        self.client.connect(self._broker_addr)
        self.client.loop_start()

    def disconnect(self):
        """Closes connection to the MQTT broker."""
        self.log.info("Disconnection process started.")
        self.client.disconnect()

        # We want to stop the network loop when:
        # 1. Client is already disconnected from the broker.
        # 2. Wait until a successful disconnection from the broker.
        while not self._disconnect_flag.is_set() and self._connected:
            self._disconnect_flag.wait(1)

        self.client.loop_stop()
        self.log.info("Disconnection process finished.")

    @property
    def connected(self):
        """Get the MQTT connection state. True, if connection was successful.
        Otherwise, false."""
        return self._connected

    @property
    def bad_connected(self):
        """Get the MQTT bad connection state. True, if connect callback was
        called, but connection failed. Otherwise, false."""
        return self._bad_connected

    def on_connect(self, client, userdata, flags, conn_rc):
        if conn_rc == 0:
            self._connected = True
            self.log.info("Connection succeeded.")
        else:
            self._bad_connected = True
            self.log.error(f"Connection encountered error, rc={conn_rc}")

    def on_disconnect(self, client, userdata, conn_rc):
        if conn_rc == 0:
            self._disconnect_flag.set()
            self.log.info("Disconnection succeeded")
        else:
            self.log.error(f"Disconnection encountered error, rc={conn_rc}")

        self._connected = False
        self._bad_connected = False

import logging

import paho.mqtt.client as mqttc

logger = logging.getLogger(__name__)


class Publisher:
    """An MQTT publisher."""

    def __init__(self, broker_addr, name=""):
        self.broker_addr = broker_addr
        self.client = mqttc.Client(name)
        self.client.enable_logger(logger)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.topic = ""

    def connect(self):
        """A non-blocking call to set up connection to the MQTT broker."""
        self.client.connect_async(self.broker_addr)
        self.client.loop_start()

    def disconnect(self):
        """Closes connection to the MQTT broker."""
        self.client.disconnect()

    def publish(self, value, qos=0):
        """Publishes a JSON string to the MQTT broker.

        :param value: the JSON string to be published.
        """
        self.client.publish(self.topic, value, qos)

    def on_connect(self, client, userdata, flags, conn_rc):
        if conn_rc == 0:
            logger.info("MQTT connection established")
        else:
            logger.error(f"MQTT connection failed, rc={conn_rc}")

    def on_disconnect(self, client, userdata, conn_rc):
        if conn_rc == 0:
            self.client.loop_stop()
            logger.info("MQTT disconnect successfully")
        else:
            logger.error(f"MQTT connection failed, rc={conn_rc}")

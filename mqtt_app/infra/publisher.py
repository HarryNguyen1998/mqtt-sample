import logging

from infra.connector import MQTTConnector

logger = logging.getLogger(__name__)


class Publisher(MQTTConnector):
    """An MQTT publisher."""

    def __init__(self, broker_addr, topic="", name="", debug=False):
        super().__init__(broker_addr, name, debug)
        self.topic = topic

    def publish(self, value, qos=0):
        """Publishes a JSON string to the MQTT broker.

        :param value: the JSON string to be published.
        """
        self.client.publish(self.topic, value, qos)

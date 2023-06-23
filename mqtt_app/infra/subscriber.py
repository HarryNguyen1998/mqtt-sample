from infra.connector import MQTTConnector

class Subscriber(MQTTConnector):
    """An MQTT subscriber."""

    def __init__(self, broker_addr, topic="", name="", debug=False):
        super().__init__(broker_addr, name, debug)
        self.topic = topic
        self.client.on_message = self.on_message

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        decoded_msg = msg.payload.decode("utf-8")
        self.log.info(f"{msg.topic}: received {decoded_msg}")

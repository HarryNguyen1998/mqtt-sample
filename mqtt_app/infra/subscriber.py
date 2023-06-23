from infra.connector import MQTTConnector
from pydantic import ValidationError
from model.charger_session import ChargerSessionModel

class Subscriber(MQTTConnector):
    """An MQTT subscriber."""

    def __init__(self, broker_addr, topic="", name="", debug=False):
        super().__init__(broker_addr, name, debug)
        self.topic = topic
        self.client.on_message = self.on_message

    def subscribe(self, topic):
        """Subscribe to the specified topic.

        :param topic: The subscribe topic.
        """
        self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        decoded_msg = msg.payload.decode("utf-8")
        try:
            # Parse the payload.
            model = ChargerSessionModel.parse_raw(decoded_msg)
            self.log.info(f"{msg.topic}: received {decoded_msg}")

            # TODO: Send to database.
        except ValidationError as ex:
            self.log.error(f"{msg.topic} failed to validate, ex={ex}")

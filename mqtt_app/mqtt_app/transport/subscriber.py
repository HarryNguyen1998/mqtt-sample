from dataclasses import dataclass

from mqtt_app.db.db import get_session
from mqtt_app.db.repository import ChargerSessionRepository
from mqtt_app.models.charger_session import ChargerSessionModel
from paho.mqtt.client import MQTT_ERR_SUCCESS
from pydantic import ValidationError
from sqlalchemy import exc

from .connector import MQTTConnector

@dataclass
class TopicAck:
    """The subscription state of the topic's subscribe id."""
    subscribe_id: int
    acknowledged: bool


class Subscriber(MQTTConnector):
    """An MQTT subscriber."""

    def __init__(self, broker_addr, name="", debug=False):
        super().__init__(broker_addr, name, debug)
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self._topic_acks: dict[str, TopicAck] = {}

    def subscribe(self, topic, qos=1):
        """Subscribe to the specified topic.

        :param topic: The subscribe topic.
        """
        self.log.info(f"Subscribing to topic={topic}")
        rc, subscribe_id = self.client.subscribe(topic, qos)
        # Early out on error.
        if rc != MQTT_ERR_SUCCESS:
            raise RuntimeError(f"Client not connected rc={rc}")

        self._topic_acks.update({topic: TopicAck(subscribe_id, False)})

    def acknowledged(self, topic: str) -> bool:
        """Whether the topic has been subscribed."""
        if not topic in self._topic_acks:
            self.log.error(f"Haven't subscribe to topic={topic}")
            return False
        return self._topic_acks[topic].acknowledged

    def on_subscribe(self, client, userdata, mid, granted_qos):
        for topic, topic_ack in self._topic_acks.items():
            if topic_ack.subscribe_id == mid:
                topic_ack.acknowledged = True
                self.log.info(f"Subscribed successfully topic={topic}")

    def on_message(self, client, userdata, msg):
        decoded_msg = msg.payload.decode("utf-8")
        try:
            # Parse the payload.
            self.log.info(
                f"Received message from topic message={decoded_msg} topic={msg.topic}"
            )
            model = ChargerSessionModel.parse_raw(decoded_msg)

            # Add payload to database.
            self.log.info(f"Adding to DB message={decoded_msg}")
            with get_session() as session:
                repo = ChargerSessionRepository(session)
                repo.create_charger_session(model)
            self.log.info(f"Added to DB successfully message={decoded_msg}")

        except ValidationError as ex:
            self.log.error(f"Failed to validate message={decoded_msg} ex={ex}")
        except exc.SQLAlchemyError as ex:
            self.log.error(f"Failed to add to DB message={decoded_msg} ex={ex.args}")

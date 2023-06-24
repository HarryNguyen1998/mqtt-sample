from mqtt_app.db.db import get_session
from mqtt_app.db.repository import ChargerSessionRepository
from mqtt_app.models.charger_session import ChargerSessionModel
from pydantic import ValidationError
from sqlalchemy import exc

from .connector import MQTTConnector


class Subscriber(MQTTConnector):
    """An MQTT subscriber."""

    def __init__(self, broker_addr, name="", debug=False):
        super().__init__(broker_addr, name, debug)
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
            self.log.info(f"Received message from topic message={decoded_msg} topic={msg.topic}")
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

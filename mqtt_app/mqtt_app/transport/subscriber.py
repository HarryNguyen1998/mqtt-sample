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
            model = ChargerSessionModel.parse_raw(decoded_msg)
            self.log.info(f"{msg.topic}: received {decoded_msg}")

            # Add payload to database.
            with get_session() as session:
                repo = ChargerSessionRepository(session)
                repo.create_charger_session(model)
            self.log.info(f"{msg.topic}: add to DB successfully.")

        except ValidationError as ex:
            self.log.error(f"{msg.topic} failed to validate, ex={ex}")
        except exc.SQLAlchemyError as ex:
            self.log.error(f"{msg.topic} failed to add to DB, ex={ex.args}")

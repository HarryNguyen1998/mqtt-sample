import logging
import random
from collections.abc import Iterator

from .charger_session import ChargerSessionModel

logger = logging.getLogger(__name__)


def charger_sessions_gen() -> Iterator[tuple[str, str]]:
    """A generator that creates new charger sessions."""
    session_counter = 1
    random_amount = random.randint(1, 100)
    while True:
        topic = f"charger/1/connector/1/session/{session_counter}"
        model = ChargerSessionModel(
            id=session_counter,
            energy_kwh=random_amount * 5,
            duration_sec=random_amount * 9,
            cost_cent=random_amount * 14,
        )
        yield (topic, model.json(by_alias=True))

        session_counter += 1
        random_amount = random.randint(1, 100)

import random
from typing import Generator

from .charger_session import ChargerSessionModel

import logging
logger = logging.getLogger(__name__)

def generate_content_stream() -> Generator[tuple[str, str], None, None]:
    """A generator that reprensents each charger session."""
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

import os


class Config:
    """Store application's configurations."""

    DB_URL = os.getenv("DB_URL", "mysql://root:root@localhost:3306/testing")
    BROKER_ADDR = os.getenv("BROKER_ADDR", "mqtt_broker")
    DEBUG_PRINT = bool(os.getenv("DEBUG_PRINT", ""))

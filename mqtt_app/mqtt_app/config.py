import os

class Config:
    DB_URL = os.getenv("DB_URL", "mysql://root:root@localhost:3306/testing")
    BROKER_ADDR = os.getenv("BROKER_ADDR", "mqtt_broker")
    DEBUG_PRINT = os.getenv("APP_DEBUG", False)

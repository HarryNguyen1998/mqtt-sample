import os


class Config:
    DB_URL = os.getenv("DB_URL", "mysql+asyncmy://root:root@localhost:3306/testing")

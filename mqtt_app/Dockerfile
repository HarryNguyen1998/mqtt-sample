FROM python:3.10-slim

EXPOSE 5000

WORKDIR /app

# Doesn't prompt graphical timezone.
ENV DEBIAN_FRONTEND=noninteractive
# Get as much info in case of crash.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    # mysqlclient requirements.
    default-libmysqlclient-dev build-essential \
    # check when DB is ready.
    curl

# Pip requirements.
COPY ./requirements.txt .

RUN pip install --upgrade pip  && \
    pip install -r requirements.txt

COPY . .

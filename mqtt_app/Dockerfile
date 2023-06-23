FROM python:3.10-slim

EXPOSE 5000

WORKDIR /app

# Doesn't prompt graphical timezone.
ENV DEBIAN_FRONTEND=noninteractive
# Get as much info in case of crash.
ENV PYTHONUNBUFFERED=1

# Installs requirements.
COPY . .

RUN pip install --upgrade pip  && \
    pip install -r requirements.txt

CMD ["python", "main.py"]

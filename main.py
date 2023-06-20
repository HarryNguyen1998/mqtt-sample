import sys
import paho.mqtt.client as mqttc

BROKER_ADDR = "mqtt_broker"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.is_connected = True
        print("MQTT connection established")
    else:
        print(f"MQTT connection failed, rc={rc}")

def main():
    client = mqttc.Client("Pub")
    client.on_connect = on_connect

    try:
        client.connect(BROKER_ADDR)
    except Exception as ex:
        print(f"Connection failed, ex={ex}")
        sys.exit(1)

    client.loop_forever()

if __name__ == "__main__":
    main()

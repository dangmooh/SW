import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    elif rc ==5:
        print("Connection refused: not authorized")
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Disconnected from broker")
    elif rc ==5:
        username = input("Enter username: ")
        password = input("Enter password: ")
        client.username_pw_set(username, password)
    elif rc != 0:
        print(f"Unexpected disconnection: {rc}")
    
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Message received on topic {msg.topic}: {payload}")
    except Exception as e:
        print(f"Error decoding message: {e}")


class MqttSubscriber:

    def __init__(self, broker_ip, username, password, topic,)
    


    def receive_message_to_broker(broker_ip, username, password, topic, port=1883):
        client = mqtt.Client()

        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

        client.username_pw_set(username, password)
        client.connect(broker_ip, port)

        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")

        client.loop_forever()


def main():
    broker_ip = "127.0.0.1"
    topic = "message"
    username = input("Enter username: ")
    password = input("Enter password: ")
    status = 'login'

    mqtt_subscriber = MqttSubscriber(broker_ip, 1883, username, password, topic, status)

    receive_message_to_broker(broker_ip, username, password, topic)

if __name__ == "__main__":
    main()

    
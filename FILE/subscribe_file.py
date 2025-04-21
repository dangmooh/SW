import paho.mqtt.client as mqtt
import os
import base64

name_topic = "updates/name"
file_topic = "updates/file"

userId = "pi"
userPw = "ekdnlt"
brokerIp = "192.168.137.151"
port = 1883
temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
os.makedirs(temp_dir, exist_ok=True)

file_name = None
file_data = None

def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("connected to broker")
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client,userdata,rc):
    print(f"Disconnected with code {rc}")

def on_message(client,userdata,msg):
    global file_name, file_data, flag
    try:
        payload = msg.payload.decode('utf-8')
        topic = msg.topic

        if topic == name_topic:
            file_name = payload

        elif topic == file_topic:
            file_data = base64.b64decode((payload))



    except Exception as e:
        print(f"Error decode message: {e}")

    if file_name and file_data:
        file_path = os.path.join(temp_dir, file_name)
        print(file_path)
        with open(file_path, 'wb')as file:
            file.write(file_data)
        print(f"File received and saved as {file_name}")
        file_name = None
        file_data = None

def receive_message_to_broker(broker_ip, username, password, topic, port = 1883):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.username_pw_set(username, password)

    client.connect(broker_ip, port = port)

    client.subscribe(topic)
    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")

    client.loop_forever()

def main():
    client = mqtt.Client()
    client.username_pw_set(userId, userPw)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(brokerIp, keepalive=60)
    client.subscribe(name_topic)
    client.subscribe(file_topic)
    client.loop_forever()

if __name__ == "__main__":
    main()
import paho.mqtt.client as mqtt
import json
import os

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from broker, code:", rc)

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")

# === MQTT 래퍼 클래스 ===
class MqttPublisher:
    def __init__(self, broker_ip, port, username, password, topic, status):
        self.topic = topic
        self.broker_ip = broker_ip
        self.port = port
        self.status = status
        self.username = username
        self.password = password
        self.user_tier = 3
        self.client = mqtt.Client()
        self.client.on_connect    = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_publish    = on_publish

        # Load user data from pwfile.json
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pwfile.json'), 'r') as f:
            self.user_data = json.load(f)

        # Load topic data from topic_tier_list.json
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'topic_tier_list.json'), 'r') as f:
            self.topic_data = json.load(f)


    def send(self, message):
        """한 번만 메시지 전송"""
        tier_key = f"Tier-{self.user_tier}"
        if tier_key in self.topic_data:
            print("Available topics:")
            for idx, topic in enumerate(self.topic_data[tier_key]["topics"], start=1):
                print(f"{idx}: {topic}")
        else:
            print(f"No topics available for Tier-{self.user_tier}.")
            return
        
        topic_idx = input("Enter topic number: ")

        try:
            topic_idx = int(topic_idx) - 1
            if 0 <= topic_idx < len(self.topic_data[tier_key]["topics"]):
                self.topic = self.topic_data[tier_key]["topics"][topic_idx]
                self.status = 'message'
            else:
                print("Invalid topic number.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
        
        self.client.publish(self.topic, message)
        self.status = 'topic'

    def connect(self):
        # Validate username and password
        if self.username in self.user_data and self.user_data[self.username]["pw"] == self.password:
            self.user_tier = self.user_data[self.username]["Tier"]
            print(f"Login successful. Your Tier: {self.user_tier}")
        else:
            print("Invalid username or password.")
            return

        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker_ip, port=self.port)
        self.client.loop_start()
        self.status = 'topic'

    def disconnect(self):
        """MQTT 연결 정리"""
        self.client.loop_stop()
        self.client.disconnect()

# === 메인 인터랙티브 루프 ===
def main():
    topic     = 'message'
    broker_ip = '127.0.0.1'
    username  = input("Enter username: ")
    password  = input("Enter password: ")
    status = 'login'

    mqtt_client = MqttPublisher(broker_ip, 1883, username, password, topic, status)

    mqtt_client.connect()

    print("\nCommands:\n"
          "  send <msg>           한 번 전송\n"
          "  exit                 종료\n")

    while True:
        cmd = input(">> ").strip()
        if cmd.lower() == 'exit':
            break
        parts = cmd.split(' ', 2)

        if parts[0] == 'send' and len(parts) == 2 and mqtt_client.status == 'topic':
            mqtt_client.send(parts[1])
        else:
            print("Unknown command")

    mqtt_client.disconnect()
    print("Program exited.")

if __name__ == "__main__":
    main()
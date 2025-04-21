import paho.mqtt.client as mqtt
import os, time
import base64
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# 설정
WATCH_DIR = "E:\\sw\\web\\upload\\"
BROKER_IP = '192.168.137.151'
PORT = 1883
USERNAME = 'pi'
PASSWORD = 'ekdnlt'
POLL_INTERVAL = 1  # (초) 폴링 기반 대안 사용 시



def make_message(file_path):
    try:
        with open(file_path, 'rb') as file:
            message = base64.b64encode(file.read())
        return message
    except FileNotFoundError as e:
        print("Error:", e)
        raise

def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print(f"Disconnected from broker, code: {rc}")

def on_publish(client,userdata, mid):
    print(f"Message {mid} published Successfully")

def send_file_to_broker(file_path, broker_ip, username, password, port=1883):

    file_name = os.path.basename(file_path)
    stem, _ = os.path.splitext(file_name)
    parts = stem.split('_', 1)
    if len(parts) == 2:
        topic_key = parts[0]
    else:
        topic_key = 'default'

    name_topic = f"{topic_key}/updates/name"
    file_topic = f"{topic_key}/updates/file"


    client = mqtt.Client()
    client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    

    client.connect(broker_ip, port=port)

    client.loop_start()

    file_name = os.path.basename(file_path)
    message = make_message(file_path)

    print(f"topic: {name_topic}, file topic : {file_topic}, file_name : {file_name}")


    client.publish(name_topic, file_name)
    client.publish(file_topic, message)

    client.loop_stop()

    print(f"success sending file(updates/name): {file_name}")
    client.disconnect()

    # 전송 후 파일 삭제
    try:
        os.remove(file_path)
        print(f"[CLEANUP] Deleted local file: {file_path}")
    except Exception as e:
        print(f"[CLEANUP ERROR] Could not delete file: {e}")

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            path = event.src_path
            # 파일이 완전히 생성될 때까지 잠시 대기
            time.sleep(0.5)
            print(f"[WATCH] New file detected: {os.path.basename(path)}")
        try:
            send_file_to_broker(path,BROKER_IP,USERNAME, PASSWORD)
        except Exception as e:
            print(f"[ERROR] Failed to send {path}: {e}")
def main():
    # 폴더 준비
    os.makedirs(WATCH_DIR, exist_ok=True)
    print(f"[WATCH] Monitoring directory: {WATCH_DIR}")

    # Watchdog 옵저버 설정
    observer = Observer()
    observer.schedule(NewFileHandler(), WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()

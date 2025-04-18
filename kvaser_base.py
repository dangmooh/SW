from canlib import canlib, Frame
import time

# Kvaser 연결 및 설정 class
class Kvaser:
    def __init__(self, channel=0):
        self.channel = channel
        self.openFlags = canlib.canOPEN_ACCEPT_VIRTUAL
        self.bitrate = canlib.canBITRATE_125K # 250까지 가능하며 500은 종단저항을 달아야 가능
        self.bitrateFlags = canlib.canDRIVER_NORMAL

        self.valid = False
        self.ch = None
        self.device_name = ''
        self.card_upc_no = ''
        try:
            self.ch = canlib.openChannel(self.channel, self.openFlags)
            self.ch.setBusOutputControl(self.bitrateFlags)
            self.ch.setBusParams(self.bitrate)
            self.ch.iocontrol.timer_scale = 1
            self.ch.iocontrol.local_txecho = True
            self.ch.busOn()
            self.valid = True
            self.device_name = canlib.ChannelData.channel_name
            self.card_upc_no = canlib.ChannelData(self.channel).card_upc_no
        except canlib.exceptions.CanGeneralError as e:
            print(f"Error initializing Kvaser channel: {e}")
            self.valid = False
            self.ch = None

    def __del__(self):
        if self.ch:
            self.tearDownChannel()


    def read(self, id, timeout_ms=-1): #CAN read 대기시간 일정 시간 지나면 종료하도록 하려면 1000이 1초인 것을 감안해서 작성
        #CAN 메시지를 읽도록 작성
        try:
            result = self.ch.read(timeout = timeout_ms)
            if result.id == id:
                return result
        except canlib.canNoMsg:
            print("No message received")
        except canlib.canError as e:
            print(f"CAN error: {e}")
        return None

    def mkdata(self, data):
        #데이터 형태를 CAN에 적합하도록 변경
        pass
      
    def transmit_data(self, id: int, data: str, msgFlag=canlib.canMSG_STD):
        #CAN 메시지 보내기
        frame = Frame(id_ = id, data = data, flags=msgFlag)
        try:
            self.ch.write(frame)
        except canlib.exceptions.CanGeneralError as e:
            print(f"Error sending Can message: {e}")

    def __iter__(self):
        while True:
            try:
                frame = self.ch.read()
                yield frame
            except canlib.canNoMsg:
                yield 0
            except canlib.canError:
                return

    def tearDownChannel(self):
        self.ch.busOff()
        self.ch.close()

def split_data_into_chunks(data, chunk_size=8):
    #큰 데이터를 CAN 전송을 위해 분할하기
    chunks = []

    total_chunks = (len(data) + chunk_size - 1) // chunk_size
    for i in range(total_chunks):
        chunk = data[i * chunk_size:(i+1) * chunk_size]
        chunks.append(chunk)

    return chunks

def transmit():
    transmitter = Kvaser()

    try:
        while True:
            data = input("Enter data to transmit: ")
            data_bytes = bytearray(data, 'utf-8')
            chunks = split_data_into_chunks(data_bytes)
            for chunk in chunks:
                transmitter.transmit_data(id=0x123, data = chunk)
                print(f"Transmitted: {chunk}")
                time.sleep(0.2)
    except KeyboardInterrupt:
        print("Interrupt received. Shutting down.")
    finally:
        del transmitter

def receive():
    receiver = Kvaser()

    try:
        while True:
            frame = receiver.read(id = 0x123)
            if frame:
                print(f"{frame.id}: {frame.data}")
    except KeyboardInterrupt:
        print("Interrupt received. Shutting down.")
    finally:
        del receiver


if __name__ == "__main__":
    transmit()
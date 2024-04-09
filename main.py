import copy
import random
import time
import threading
import queue
import serial
import traceback

exp_list = [
    ["A1", "A2", "A3", "A4", "A5", ],
    ["A6", "A7", "A8", "B1", "B2", ],
    ["B3", "B4", "B5", "B6", "B7", ],
    ["B8", "C1", "C2", "D1", "D2", ],
    ["D3", "D4", "D5", "D6", "D7", ],
    ["D8", "E1", "E2", "E3", "E4", ],
    ["E5", "E6", "E7", "E8", ],
]


class SerialManager:
    p1Serial = serial.Serial("COM33", 9600)
    # p2Serial = serial.Serial("COM44", 9600)
    settingPacket = bytearray([40, 0, 0, 0, 0, 41])
    touchData = bytearray([40, 0, 0, 0, 0, 0, 0, 0, 41])
    touchData2 = bytearray([40, 0, 0, 0, 0, 0, 0, 0, 41])
    startUp = False
    recvData = ""

    def __init__(self):
        self.touchQueue = queue.Queue()
        self.touchThread = threading.Thread(target=self.touch_thread)
        self.ping_touch_thread()

    def start(self):
        print("开始监听 COM33 串口...")
        self.touchThread.start()

    def ping_touch_thread(self):
        self.touchQueue.put([True, self.build_touch_package(exp_list)])

    def touch_thread(self):
        while True:
            # start_time = time.time()
            if self.p1Serial.is_open:
                self.read_data(self.p1Serial)
            # if self.p2Serial.is_open:
            #     self.read_data(self.p2Serial)
            if not self.touchQueue.empty():
                # print("touchQueue 不为空，开始执行")
                s_temp = self.touchQueue.get()
                self.update_touch(s_temp)
            time.sleep(0.00001)
            # print(f"单次循环执行时间：{time.time() - start_time}秒")

    def destroy(self):
        self.touchThread.join()
        self.p1Serial.close()
        # self.p2Serial.close()

    def read_data(self, ser):
        if ser.in_waiting == 6:
            self.recvData = ser.read(6).decode()
            print(self.recvData)
            self.touch_setup(ser, self.recvData)

    def touch_setup(self, ser, data):
        byte_data = ord(data[3])
        if byte_data in [76, 69]:
            self.startUp = False
        elif byte_data in [114, 107]:
            for i in range(1, 5):
                self.settingPacket[i] = ord(data[i])
            ser.write(self.settingPacket)
        elif byte_data == 65:
            self.startUp = True

    def send_touch(self, ser, data):
        ser.write(data)

    def build_touch_package(self, sl):
        sum_list = [0, 0, 0, 0, 0, 0, 0]
        for i in range(len(sl)):
            for j in range(len(sl[i])):
                if sl[i][j] == 1:
                    sum_list[i] += (2 ** j)
        s = "28 "
        for i in sum_list:
            s += hex(i)[2:].zfill(2).upper() + " "
        s += "29"
        print(s)
        return bytes.fromhex(s)

    def update_touch(self, s_temp):
        # if not self.startUp:
        #     print("当前没有启动")
        #     return
        if s_temp[0]:
            self.send_touch(self.p1Serial, s_temp[1])
        # else:
        #     self.send_touch(self.p2Serial, s_temp[1])

    def change_touch(self, is_p1, sl):
        self.touchQueue.put([is_p1, self.build_touch_package(sl)])


if __name__ == "__main__":
    serial_manager = SerialManager()
    serial_manager.start()
    input()
    while True:
        try:
            start_time = time.time()
            kk = copy.deepcopy(exp_list)
            for ik, vk1 in enumerate(kk):
                for jk, vk2 in enumerate(vk1):
                    kk[ik][jk] = random.choice([0, 1])
            serial_manager.change_touch(True, kk)
            print(f"代码执行时间：{time.time() - start_time}秒")
            time.sleep(0.1)
        except:
            print("出现错误")
            time.sleep(1)

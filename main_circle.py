from PIL import Image
import subprocess
import copy
import time
import threading
import queue
import serial

# 串口号
COM_PORT = "COM33"
# 比特率
COM_BAUDRATE = 9600
# Android 多点触控数量
MAX_SLOT = 12
# 检测区域的像素值范围
AREA_SCOPE = 85

exp_image = Image.open("./image_monitor.png")
exp_image_width, exp_image_height = exp_image.size

exp_list = [
    ["A1", "A2", "A3", "A4", "A5", ],
    ["A6", "A7", "A8", "B1", "B2", ],
    ["B3", "B4", "B5", "B6", "B7", ],
    ["B8", "C1", "C2", "D1", "D2", ],
    ["D3", "D4", "D5", "D6", "D7", ],
    ["D8", "E1", "E2", "E3", "E4", ],
    ["E5", "E6", "E7", "E8", ],
]
exp_image_dict = {
    "61": "A1", "65": "A2", "71": "A3", "75": "A4", "81": "A5", "85": "A6", "91": "A7", "95": "A8",
    "101": "B1", "105": "B2", "111": "B3", "115": "B4", "121": "B5", "125": "B6", "130": "B7", "135": "B8",
    "140": "C1", "145": "C2",
    "150": "D1", "155": "D2", "160": "D3", "165": "D4", "170": "D5", "175": "D6", "180": "D7", "185": "D8",
    "190": "E1", "195": "E2", "200": "E3", "205": "E4", "210": "E5", "215": "E6", "220": "E7", "225": "E8",
}


class SerialManager:
    p1Serial = serial.Serial(COM_PORT, COM_BAUDRATE)
    # p2Serial = serial.Serial("COM44", 9600)
    settingPacket = bytearray([40, 0, 0, 0, 0, 41])
    startUp = False
    recvData = ""

    def __init__(self):
        self.touchQueue = queue.Queue()
        self.data_lock = threading.Lock()
        self.touchThread = threading.Thread(target=self.touch_thread)
        self.writeThread = threading.Thread(target=self.write_thread)
        self.now_touch_data = b''
        self.now_touch_keys = []
        self.ping_touch_thread()

    def start(self):
        print("开始监听 COM33 串口...")
        self.touchThread.start()
        self.writeThread.start()

    def ping_touch_thread(self):
        self.touchQueue.put([self.build_touch_package(exp_list), []])

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
            # 延迟防止 CPU 时间过长
            time.sleep(0.0001)
            # print(f"单次循环执行时间：{time.time() - start_time}秒")

    def write_thread(self):
        while True:
            # 延迟匹配波特率
            time.sleep(0.01)  # 9600
            # time.sleep(0.002)  # 115200
            if not self.startUp:
                # print("当前没有启动")
                continue
            # print(self.now_touch_data)
            with self.data_lock:
                self.send_touch(self.p1Serial, self.now_touch_data)

    def destroy(self):
        self.touchThread.join()
        self.p1Serial.close()
        # self.p2Serial.close()

    def read_data(self, ser):
        if ser.in_waiting == 6:
            self.recvData = ser.read(6).decode()
            # print(self.recvData)
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
            print("已连接到游戏")
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
        # print(s)
        return bytes.fromhex(s)

    def update_touch(self, s_temp):
        # if not self.startUp:
        #     print("当前没有启动")
        #     return
        with self.data_lock:
            self.now_touch_data = s_temp[0]
            self.send_touch(self.p1Serial, s_temp[0])
            self.now_touch_keys = s_temp[1]
        print("Touch Keys:", s_temp[1])
        # else:
        #     self.send_touch(self.p2Serial, s_temp[0])

    def change_touch(self, sl, touch_keys):
        self.touchQueue.put([self.build_touch_package(sl), touch_keys])


def get_colors_in_area(x, y):
    colors = set()  # 使用集合来存储颜色值，以避免重复
    for dx in [-AREA_SCOPE, 0, AREA_SCOPE]:
        for dy in [-AREA_SCOPE, 0, AREA_SCOPE]:
            if 0 <= (x + dx) < exp_image_width and 0 <= (y + dy) < exp_image_height:
                colors.add(str(exp_image.getpixel((x + dx, y + dy))[0]))
    return list(colors)


def convert(touch_data):
    copy_exp_list = copy.deepcopy(exp_list)
    touch_keys = set()
    for i in touch_data:
        if not i["p"]:
            continue
        x = i["x"]
        y = i["y"]
        for r_str in get_colors_in_area(x, y):
            if not r_str in exp_image_dict:
                continue
            touch_keys.add(exp_image_dict[r_str])
    # print("Touch Keys:", touch_keys)
    touch_keys_list = list(touch_keys)
    for i in range(len(copy_exp_list)):
        for j in range(len(copy_exp_list[i])):
            if copy_exp_list[i][j] in touch_keys_list:
                copy_exp_list[i][j] = 1
            else:
                copy_exp_list[i][j] = 0
    # print(copy_exp_list)
    serial_manager.change_touch(copy_exp_list, touch_keys_list)


def getevent():
    # 存储多点触控数据的列表
    touch_data = [{"p": False, "x": 0, "y": 0} for _ in range(MAX_SLOT)]
    # 记录当前按下的触控点数目
    touch_sum = 0
    # 记录当前选择的 SLOT 作为索引
    touch_index = 0

    # 执行 adb shell getevent 命令并捕获输出
    process = subprocess.Popen(['adb', 'shell', 'getevent', '-l'], stdout=subprocess.PIPE)
    key_is_changed = False

    # 读取实时输出
    for line in iter(process.stdout.readline, b''):
        try:
            event = line.decode('utf-8').strip()
            _, _, event_type, event_value = event.split()
            if event_type == 'ABS_MT_POSITION_X':
                key_is_changed = True
                touch_data[touch_index]["x"] = int(event_value, 16)
            elif event_type == 'ABS_MT_POSITION_Y':
                key_is_changed = True
                touch_data[touch_index]["y"] = int(event_value, 16)
            elif event_type == 'SYN_REPORT':
                if not key_is_changed:
                    continue
                # print("Touch Data:", touch_data)
                # 向 convert 函数发送数据
                key_is_changed = False
                # start_time = time.time()
                convert(touch_data)
                # print(f"代码执行时间：{time.time() - start_time}秒")
            elif event_type == 'ABS_MT_SLOT':
                key_is_changed = True
                touch_index = int(event_value, 16)
                if touch_index >= touch_sum:
                    touch_sum = touch_index + 1
            elif event_type == 'ABS_MT_TRACKING_ID':
                key_is_changed = True
                if event_value == "ffffffff":
                    touch_data[touch_index]['p'] = False
                    touch_sum -= 1
                    if touch_sum < 0:
                        touch_sum = 0
                else:
                    touch_data[touch_index]['p'] = True
                    touch_sum += 1
            else:
                continue
        except Exception:
            event_error_output = line.decode('utf-8')
            if "name" in event_error_output:
                continue
            print(event_error_output)


if __name__ == "__main__":
    serial_manager = SerialManager()
    serial_manager.start()
    getevent()

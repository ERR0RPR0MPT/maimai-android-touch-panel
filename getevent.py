from PIL import Image
import subprocess
import copy
import time

max_slot = 12

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


def convert(touch_data):
    copy_exp_list = copy.deepcopy(exp_list)
    touch_keys = []
    for i in touch_data:
        if not i["p"]:
            continue
        x = i["x"]
        y = i["y"]
        if 0 <= x < exp_image_width and 0 <= y < exp_image_height:
            rgb = exp_image.getpixel((x, y))
            r_str = str(rgb[0])
            if not r_str in exp_image_dict:
                continue
            touch_keys.append(exp_image_dict[r_str])
        else:
            print("Coordinates ({}, {}) are out of image bounds.".format(x, y))
    print("Touch Keys:", touch_keys)
    for i in range(len(copy_exp_list)):
        for j in range(len(copy_exp_list[i])):
            if copy_exp_list[i][j] in touch_keys:
                copy_exp_list[i][j] = 1
            else:
                copy_exp_list[i][j] = 0
    # print(copy_exp_list)



def getevent():
    # 存储多点触控数据的列表
    touch_data = [{"p": False, "x": 0, "y": 0} for _ in range(max_slot)]
    # 记录当前按下的触控点数目
    touch_sum = 0
    # 记录当前选择的 SLOT 作为索引
    touch_index = 0

    # 执行 adb shell getevent 命令并捕获输出
    process = subprocess.Popen(['adb', 'shell', 'getevent', '-l'], stdout=subprocess.PIPE)

    # 读取实时输出
    for line in iter(process.stdout.readline, b''):
        try:
            event = line.decode('utf-8').strip()
            _, _, event_type, event_value = event.split()
            if event_type == 'ABS_MT_POSITION_X':
                touch_data[touch_index]["x"] = int(event_value, 16)
            elif event_type == 'ABS_MT_POSITION_Y':
                touch_data[touch_index]["y"] = int(event_value, 16)
            elif event_type == 'SYN_REPORT':
                # print("Touch Data:", touch_data)
                # 向 convert 函数发送数据
                start_time = time.time()
                convert(touch_data)
                print(f"代码执行时间：{time.time() - start_time}秒")
            elif event_type == 'ABS_MT_SLOT':
                touch_index = int(event_value, 16)
                if touch_index >= touch_sum:
                    touch_sum = touch_index + 1
            elif event_type == 'ABS_MT_TRACKING_ID':
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
            print(line.decode('utf-8'))
            pass


if __name__ == "__main__":
    getevent()

import time


def microsecond_sleep(sleep_time):
    end_time = time.perf_counter() + (sleep_time - 1.0) / 1e6  # 1.0是时间补偿，需要根据自己PC的性能去实测
    while time.perf_counter() < end_time:
        pass


start = time.perf_counter()
microsecond_sleep(10)  # 等待10微秒
end = time.perf_counter()
print(start)
print(end)
print("等待时间:", (end-start) * 1e6, "微秒")

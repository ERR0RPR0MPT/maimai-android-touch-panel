# maimai-android-touch-panel

使用 `adb shell getevent` 记录 Android 设备触屏事件并模拟 maimai 触摸屏幕的脚本.

## 使用方法

1. 打开任意P图工具, 准备一个和设备屏幕大小相同的一张图片(例如:1600x2560), 将 `./image/color_exp_panel.png`
放置到该图片圆形触摸区域的位置(或者可以参考`./image/image_monitor_edit3.png`的做法), 编辑好的图片放到脚本目录下取名 `image_monitor.png`.
2. 编辑 `main.py` 脚本文件, 修改脚本内 `exp_image_dict` 变量, 将各区块对应的 R 通道颜色值改为刚P的图的对应区块颜色值(一般不用改默认就行)
3. 编辑 `main.py` 脚本文件, 修改脚本内 `COM_PORT`, `COM_BAUDRATE`, `MAX_SLOT` 三个配置
4. 下一个 `VSPD` 虚拟串口工具, 将 `COM3` 和 `COM33` 建立转发
5. 电脑安装 ADB 调试工具, 安装路径添加到系统环境变量里面
6. 手机打开 USB 调试, 强烈建议同时使用 USB 网络共享连接电脑, 串流走 WLAN 可能不是很稳定
7. 电脑画面可使用 `IddSampleDriver`, `Sunshine` 和 `Moonlight` 等串流到 Android 设备, 这里不再赘述
8. 手机连接电脑, 先运行脚本 `python main.py`, 再运行游戏, 脚本控制台输出 `已连接到游戏` 即可
9. 进游戏调整延迟, 一般判定A/B都要调才能正常用, 我这边是 `A:-1.0/B:0.5`
10. 打一把看看蹭不蹭星星/触控是否灵敏, 根据体验修改 `AREA_SCOPE` 变量即可(默认65)
11. 如果单点延迟低但滑动时延迟变高, 请将脚本中 `TOUCH_THREAD_SLEEP_MODE` 修改为 False, 
或者可以调小 `TOUCH_THREAD_SLEEP_DELAY` 的值

## 注意

想要加 2P 的重新复制一下脚本并添加串口 COM4 到 COM44 的转发就好

该脚本仅用于测试, 目前来说打12+及以下应该是问题不大, 12+以上水平不够没试过.

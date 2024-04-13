# maimai-android-touch-panel

使用 `adb shell getevent` 记录 Android 设备触屏事件并模拟 maimai 触摸屏幕的脚本.

## 使用方法

1. 打开任意P图工具, 准备一个和设备屏幕大小相同的一张图片(例如:1600x2560), 将 `./image/color_exp_panel.png`
   放置到该图片圆形触摸区域的位置(或者可以参考`./image/image_monitor_edit3.png`的做法), 编辑好的图片放到脚本 `image`
   目录下取名 `image_monitor.png`.
2. 编辑 `main.py` 脚本文件, 修改脚本内 `exp_image_dict` 变量, 将各区块对应的 R 通道颜色值改为刚P的图的对应区块颜色值(
   一般不用改默认就行)
3. 电脑安装 ADB 调试工具, 安装路径添加到系统环境变量里面
4. 运行 `adb shell getevent -l`, 点一下屏幕的最右下角的位置, 在终端获取 `ABS_MT_POSITION_X` 和 `ABS_MT_POSITION_Y`
   两个的数值,
   把十六进制转换到十进制, 将原本的屏幕大小填入脚本内 `ANDROID_ABS_MONITOR_SIZE` 配置,
   将触摸右下角得到的数据填入到 `ANDROID_ABS_INPUT_SIZE` 配置
5. Android 设备充电口朝下一般为屏幕的正向, 如需反向屏幕游玩可将脚本内 `ANDROID_REVERSE_MONITOR` 改为 True
6. 编辑 `main.py` 脚本文件, 修改脚本内 `IMAGE_PATH` `COM_PORT`, `COM_BAUDRATE`, `MAX_SLOT` 四个配置
7. 下一个 `VSPD` 或 `com0com` 虚拟串口工具, 将 `COM3` 和 `COM33` 建立转发
8. 手机打开 USB 调试, 强烈建议同时使用 USB 网络共享连接电脑, 串流走 WLAN 可能不是很稳定
9. 电脑画面可使用 `IddSampleDriver`, `Sunshine` 和 `Moonlight` 或者延迟较大但比较方便的 `spacedesk` 等串流到 Android 设备,
   详细过程请自行寻找, 不在本篇讨论范围之内
10. 手机连接电脑, 先运行脚本 `python main.py`, 再运行游戏, 脚本控制台输出 `已连接到游戏` 即可
11. 进游戏调整延迟, 一般判定A/B都要调才能正常用, 我这边是 `A:-1.0/B:+0.5` 到 `A:-2.0/B:+2.0`
12. 打一把看看蹭不蹭星星/触控是否灵敏, 根据体验修改 `AREA_SCOPE` 变量即可(默认65)
13. 如果单点延迟低但滑动时延迟变高, 请将脚本中 `TOUCH_THREAD_SLEEP_MODE` 修改为 False,
    或者可以调小 `TOUCH_THREAD_SLEEP_DELAY` 的值

游戏时如果不小心断开连接, 请在控制台输入 `start` 并回车来重新连接游戏

## 部分问题

Q: 在安卓高版本(13,14)上测试触摸区域完全对不上，只有点屏幕左上角有用，图片用的是平板实际分辨率，在一台安卓10设备测试是正常的

A: 按步骤修改脚本内 `ANDROID_ABS_MONITOR_SIZE` 和 `ANDROID_ABS_INPUT_SIZE` 配置

## 注意

想要加 2P 的重新复制一下脚本并添加串口 COM4 到 COM44 的转发就好

该脚本仅用于测试, 目前来说打12+及以下应该是问题不大, 12+以上水平不够没试过.

## 其他

P区块图的成品类似这样:

![](https://raw.githubusercontent.com/ERR0RPR0MPT/maimai-android-touch-panel/main/image/image_monitor.png)

# maimai-android-touch-panel

使用 `adb shell getevent` 记录 Android 设备触屏事件并模拟 maimai 触摸屏幕的脚本.

## 提示
非常感谢原作者提供的脚本，本 fork 針對为小米平板6 Pro進行了更好的优化，同时提供紧凑模式设置以避免滑到底栏而中途破防？


玩具项目，~~仅在 Xiaomi Pad 5 Pro (Android 13) 上通过测试~~,
且仅适配了 Linux 多点触控协议类型 B .

目前已知的问题有:

- 仅支持 Linux 多点触控协议类型 B 而不支持 A (#6)，这可能会导致较旧的设备不受支持,
  两种类型不同之处详见[文档](https://www.kernel.org/doc/Documentation/input/multi-touch-protocol.txt)
- 输出 Touch Keys 但无按键按下(分辨率问题)
- 游戏内按两下只识别一个 tap(脚本未进入运行模式)
- 游戏内始终显示按下(未知原因)

本人暂无时间去修复存在的 Bug，对于 open issue 和 B 站私信问题的很抱歉本人无法进行答复,
有能力的可以自行修复，也欢迎提交 PR.

另外本项目使用了效率较为低下且抽象的方案(Python+读图+串流)，存在延迟等问题，由于本身是娱乐项目故未做优化.

更加优秀的项目有:

- [KanadeDX](https://github.com/KanadeDX/Public) (某八个按键程序在 Android/iOS 上的实现)
- [AstroDX](https://github.com/2394425147/astrodx) (Android，Windows?)
- [MajdataPlay](https://github.com/LingFeng-bbben/MajdataPlay) (Windows，Android?)

这些项目包含对 Mai2 Chart Player 的完整实现，而不仅仅是一个触摸输入程序.

## 使用方法

1. 请先将游戏配置文件中 `DummyTouchPanel` 的值改为 `0`
2. 打开任意 P 图工具，准备一个和设备屏幕大小相同的一张图片(例如:1600x2560)，将 `./image/color_exp_panel.png`
   放置到该图片圆形触摸区域的位置，编辑好的图片放到脚本 `image` 目录下取名 `image_monitor.png`.
3. 编辑 `config.yaml` 配置文件，修改 `exp_image_dict` 配置，将各区块对应的 RGB 通道颜色值改为刚 P 的图的对应区块颜色值（一般不用改，默认就行）
4. 电脑安装 ADB 调试工具，安装路径添加到系统环境变量里面
5. 如果电脑上没有 Python 环境，请先去 [官网](https://www.python.org/) 下载安装
6. 双击运行 `install.bat` 安装依赖
7. 先将实际屏幕大小填入脚本内 `ANDROID_ABS_MONITOR_SIZE` 配置，打开终端，运行 `adb shell getevent -l`，点一下屏幕的最右下角的位置，在终端获取该次点击得到的 `ABS_MT_POSITION_X` 和 `ABS_MT_POSITION_Y` 的数值，把十六进制转换到十进制，将得到的数据填入到 `ANDROID_ABS_INPUT_SIZE` 配置
8. Android 设备充电口朝下一般为屏幕的正向，如需反向屏幕游玩可将配置 `ANDROID_REVERSE_MONITOR` 改为 true
9. 编辑 `config.yaml` 配置文件，按文件内说明修改多个配置
10. 下载一个 `VSPD` 虚拟串口工具，将 `COM3` 和 `COM33` 建立转发
11. 手机打开 USB 调试，强烈建议同时使用 USB 网络共享连接电脑，串流走 WLAN 可能不是很稳定
12. 电脑画面可使用 `Apollo`，`IddSampleDriver`，`Sunshine` 和 `Moonlight` 或者延迟较大但比较方便的 `spacedesk` 等软件串流到 Android 设备，详细过程请自行寻找，不在本篇讨论范围之内
13. 手机连接电脑，先双击运行 `start.bat`，再运行游戏，脚本控制台输出 `已连接到游戏` 即可
14. 进游戏调整延迟，一般判定 A/B 都要调才能正常用，我这边是 `A:-1.0/B:+0.5` 到 `A:-2.0/B:+2.0`
15. 打一把看看蹭不蹭星星/触控是否灵敏，根据体验修改 `AREA_SCOPE` 变量 c'c'x'c'c'z'z'z'z'd'd'd'd'c'x
16. 如果单点延迟低但滑动时延迟极大，请将脚本中 `TOUCH_THREAD_SLEEP_MODE` 修改为 false，或者可以调小 `TOUCH_THREAD_SLEEP_DELAY` 的值(如果还是卡请提交 issue 反馈)


## 命令列表

游戏时如果不小心断开连接，请在控制台输入 `start` 并回车来重新连接游戏

输入 `reverse` 可调整触控设备屏幕方向

输入 `restart` 可重新读取配置文件/重启脚本

输入 `exit` 可完全退出脚本

## 部分问题

关于延迟/其他建议可参考 [#3](https://github.com/ERR0RPR0MPT/maimai-android-touch-panel/issues/3)

Q：在安卓高版本(13,14)上测试触摸区域完全对不上，只有点屏幕左上角有用，图片用的是平板实际分辨率，在一台安卓 10 设备测试是正常的

A：按步骤修改脚本内 `ANDROID_ABS_MONITOR_SIZE` 和 `ANDROID_ABS_INPUT_SIZE` 配置

Q：关闭再打开报错

A：如果直接关闭控制台窗口有可能导致后台进程残留，请使用任务管理器彻底关闭进程或者使用 Ctrl + C 终止程序，也可以在退出前输入 `exit` 。

## 注意

想要加 2P 的重新复制一下脚本并添加串口 COM4 到 COM44 的转发，并且在配置文件 “SPECIFIED_DEVICES” 中指定使用 “adb devices” 获取到的设备序列号

~~该脚本仅用于测试，目前来说打 12+ 及以下应该是问题不大，12+ 以上水平不够没试过.~~
本人测试后，打 12-13 也可以鸟加，13+ 以上开始容易断，需要在之后进行更好的优化。

## 类似项目

[maimai-windows-touch-panel](https://github.com/ERR0RPR0MPT/maimai-windows-touch-panel)

## 许可证

[MIT License](https://github.com/ERR0RPR0MPT/maimai-android-touch-panel?tab=MIT-1-ov-file)

## 其他

编辑好的区块成品图类似这样：

![](https://raw.githubusercontent.com/ERR0RPR0MPT/maimai-android-touch-panel/main/image/image_monitor.png)
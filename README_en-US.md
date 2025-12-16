# maimai-android-touch-panel

English | [简体中文](README.md)

A script that records Android device touch events using `adb shell getevent` and simulates maimai touch panel input.

## Notice
This is a small project tested on Xiaomi Pad 5 Pro (Android 13) and Xiaomi Pad 6 Pro (Android 15), and only supports Linux multi-touch protocol Type B.

Known issues:

- Only supports Linux multi-touch protocol Type B, not Type A (#6), which may cause older devices to be unsupported.
  For differences between the two types, see [documentation](https://www.kernel.org/doc/Documentation/input/multi-touch-protocol.txt)
- Touch Keys output but no key press detected (resolution issue)
- Double tap in-game only registers once (script not in running mode)
- Touch always shows as pressed in-game (unknown cause)

I currently don't have time to fix existing bugs. Sorry for not being able to respond to open issues and Bilibili private messages.
Those who are capable can fix them on their own, and PRs are welcome.

Additionally, this project uses an inefficient and abstract approach (Python + image reading + streaming), which has latency issues. Since it's an entertainment project, no optimization has been done.

Better projects include:

- [KanadeDX](https://github.com/KanadeDX/Public) (Implementation of a certain 8-button program on Android/iOS)
- [AstroDX](https://github.com/2394425147/astrodx) (Android, Windows?)
- [MajdataPlay](https://github.com/LingFeng-bbben/MajdataPlay) (Windows, Android?)

These projects include complete implementations of Mai2 Chart Player, not just a touch input program.

## Usage

1. First, change the value of `DummyTouchPanel` in the game configuration file to `0`
2. Open any image editing tool and prepare an image with the same size as your device screen (e.g., 1600x2560). Place `./image/color_exp_panel.png` at the circular touch area position of the image. Save the edited image to the script's `image` directory and name it `image_monitor.png`
3. Edit the `config.yaml` configuration file. Modify the `exp_image_dict` configuration to change the RGB channel color values of each zone to match your edited image's corresponding zone colors (usually no need to change, default is fine)
4. Install ADB debugging tools on your computer and add the installation path to system environment variables
5. If you don't have Python installed, download and install it from the [official website](https://www.python.org/)
6. Double-click `install.bat` to install dependencies
7. First, fill in the actual screen size into the `ANDROID_ABS_MONITOR_SIZE` configuration in the script. Open a terminal, run `adb shell getevent -l`, tap the bottom-right corner of the screen, get the `ABS_MT_POSITION_X` and `ABS_MT_POSITION_Y` values from the terminal, convert hexadecimal to decimal, and fill the obtained data into the `ANDROID_ABS_INPUT_SIZE` configuration
8. Android devices with charging port facing down are generally in normal screen orientation. If you need to play with reversed screen, change the `ANDROID_REVERSE_MONITOR` configuration to true
9. Edit the `config.yaml` configuration file and modify multiple configurations according to the instructions in the file
10. Download a `VSPD` virtual serial port tool and establish forwarding between `COM3` and `COM33`
11. Enable USB debugging on your phone. Strongly recommend using USB network tethering to connect to the computer, as streaming over WLAN may not be very stable and increase latency
12. You can stream the computer screen to Android devices using software like `Apollo`, `IddSampleDriver`, `Sunshine` and `Moonlight`, or the more convenient but higher latency `spacedesk`. Please find the detailed process on your own, as it's not within the scope of this discussion
13. Connect your phone to the computer, first double-click `start.bat`, then run the game. When the script console outputs `已连接到游戏` (Connected to game), you're ready
14. Adjust the delay in-game. Generally, both judgment A/B need adjustment to work properly. For me, it's `A:-1.0/B:+0.5` to `A:-2.0/B:+2.0`
15. Play a round to see if you're missing any slides / if touch is responsive. Modify the `AREA_SCOPE` variable based on your experience
16. If single-point latency is low but sliding has extremely high latency, change `TOUCH_THREAD_SLEEP_MODE` in the script to false, or you can decrease the value of `TOUCH_THREAD_SLEEP_DELAY` (if it's still laggy, please submit an issue for feedback)

## Command List

If accidentally disconnected during gameplay, enter `start` in the console and press Enter to reconnect to the game

Enter `reverse` to adjust the touch device screen orientation

Enter `restart` to reload the configuration file/restart the script

Enter `exit` to fully exit the script

## Common Issues

For delay/other suggestions, refer to [#3](https://github.com/ERR0RPR0MPT/maimai-android-touch-panel/issues/3)

Q: On higher Android versions (13-15), the touch area is completely misaligned. Only tapping the top-left corner of the screen works. The image uses the tablet's actual resolution. Testing on an Android 10 device works normally.

A: Follow the steps to modify the `ANDROID_ABS_MONITOR_SIZE` and `ANDROID_ABS_INPUT_SIZE` configurations in the script

Q: Error when closing and reopening

A: Directly closing the console window may cause background processes to remain. Please use Task Manager to completely close the process or use Ctrl + C to terminate the program. You can also enter `exit` before exiting.

## Notes

To add 2P, copy the script again and add forwarding from COM4 to COM44. In the configuration file "SPECIFIED_DEVICES", specify the device serial number obtained using "adb devices"

This script is for testing purposes only. Currently, playing 12-13 difficulty is feasible and need better optimization in the future.

## Similar Projects

[maimai-windows-touch-panel](https://github.com/ERR0RPR0MPT/maimai-windows-touch-panel)

## License

[MIT License](https://github.com/ERR0RPR0MPT/maimai-android-touch-panel?tab=MIT-1-ov-file)

## Other

The edited zone image should look something like this:

![](https://raw.githubusercontent.com/ERR0RPR0MPT/maimai-android-touch-panel/main/image/image_monitor.png)

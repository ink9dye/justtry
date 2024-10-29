import pyautogui
import time
import json
from pynput import keyboard
import ctypes
import sys

# 检查管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 如果不是管理员权限，则申请管理员权限
if not is_admin():
    # 重新启动脚本并申请管理员权限
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()  # 退出当前实例，等待新实例启动

# 禁用 DPI 感知
ctypes.windll.user32.SetProcessDPIAware()

# 全局变量控制回放是否停止
stop_replay = False

# 获取当前屏幕分辨率
screen_width, screen_height = pyautogui.size()

# 停止回放的按键处理函数
def on_press(key):
    global stop_replay
    if hasattr(key, 'char') and key.char and key.char.lower() == 'a':
        stop_replay = True
        print("回放停止中...")

# 回放录制
def replay_actions():
    global stop_replay
    print("开始回放... 按下 'A' 停止回放。")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        with open(r"E:\pythons\pyex2\recorded_actions.json", "r") as f:
            actions = json.load(f)
    except FileNotFoundError:
        print("未找到录制文件 recorded_actions.json，请先运行 record.py 进行录制。")
        return

    speed_multiplier = 1 / 2  # 两倍速
    start_time = time.time()

    for action in actions:
        if stop_replay:
            print("回放已停止。")
            break

        adjusted_timestamp = action["timestamp"] * speed_multiplier
        time_to_sleep = max(0, adjusted_timestamp - (time.time() - start_time))
        time.sleep(time_to_sleep)

        # 执行动作，将相对位置转换回实际像素坐标
        if action["type"] == "mouse_click":
            x = int(action["position"][0] * screen_width)
            y = int(action["position"][1] * screen_height)
            pyautogui.moveTo(x, y)
            if action["pressed"]:
                pyautogui.mouseDown(button=action["button"].split(".")[-1])
            else:
                pyautogui.mouseUp(button=action["button"].split(".")[-1])
        elif action["type"] == "mouse_move":
            x = int(action["position"][0] * screen_width)
            y = int(action["position"][1] * screen_height)
            pyautogui.moveTo(x, y, duration=0.1)
        elif action["type"] == "key_press":
            pyautogui.press(action["key"].replace("'", ""))
        elif action["type"] == "wait":
            time.sleep(action["duration"])

    print("回放完成。")
    listener.stop()

if __name__ == "__main__":
    replay_actions()

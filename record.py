# record_actions.py
from pynput import mouse, keyboard
import time
import json
import os

# 存储动作的列表
actions = []
# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "recorded_actions.json")
# 记录开始时间
start_time = None
stop_recording = False  # 全局变量用于控制停止录制

# 鼠标事件处理
def on_click(x, y, button, pressed):
    global start_time
    if start_time is None:
        start_time = time.time()
    timestamp = time.time() - start_time
    action = {
        "type": "mouse_click",
        "position": (x, y),
        "button": str(button),
        "pressed": pressed,
        "timestamp": timestamp
    }
    actions.append(action)

def on_move(x, y):
    global start_time
    if start_time is None:
        start_time = time.time()
    timestamp = time.time() - start_time
    action = {
        "type": "mouse_move",
        "position": (x, y),
        "timestamp": timestamp
    }
    actions.append(action)

# 键盘事件处理
def on_press(key):
    global start_time, stop_recording
    if start_time is None:
        start_time = time.time()
    timestamp = time.time() - start_time
    action = {
        "type": "key_press",
        "key": str(key),
        "timestamp": timestamp
    }
    actions.append(action)

    # 如果按下 'A' 键则停止录制
    if hasattr(key, 'char') and key.char and key.char.lower() == 'a':
        stop_recording = True  # 设置停止标志

def on_release(key):
    global start_time
    if start_time is None:
        start_time = time.time()
    timestamp = time.time() - start_time
    action = {
        "type": "key_release",
        "key": str(key),
        "timestamp": timestamp
    }
    actions.append(action)

# 开始录制
def start_recording():
    global stop_recording
    print("开始录制... 按下字母 'A' 停止录制（不区分大小写）。")

    # 创建监听器
    with mouse.Listener(on_click=on_click, on_move=on_move) as mouse_listener, \
         keyboard.Listener(on_press=on_press, on_release=on_release) as keyboard_listener:

        # 循环检查是否需要停止录制
        while not stop_recording:
            time.sleep(0.1)

        # 停止监听器
        mouse_listener.stop()
        keyboard_listener.stop()

    print("录制完成。")

    # 将动作保存到文件
    with open(file_path, "w") as f:
        json.dump(actions, f)
    print("动作已保存到", file_path)

if __name__ == "__main__":
    start_recording()
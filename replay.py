import pyautogui
import time
import json
from pynput import keyboard

# 全局变量控制回放是否停止
stop_replay = False

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

    move_count = 0  # 记录五秒内的移动次数
    last_reset_time = time.time()  # 用于重置计数
    action_interval = 5  # 每五秒内最多五次移动

    for action in actions:
        if stop_replay:
            print("回放已停止。")
            break

        adjusted_timestamp = action["timestamp"] * speed_multiplier
        time_to_sleep = max(0, adjusted_timestamp - (time.time() - start_time))
        time.sleep(time_to_sleep)

        current_time = time.time()

        # 每五秒内最多五次移动
        if current_time - last_reset_time > action_interval:
            move_count = 0
            last_reset_time = current_time

        # 执行鼠标和键盘动作
        if action["type"] == "mouse_click":
            x, y = action["position"]
            pyautogui.moveTo(x, y)  # 保证点击前位置精确
            if action["pressed"]:
                pyautogui.mouseDown(x=x, y=y, button=action["button"].split(".")[-1])
            else:
                pyautogui.mouseUp(x=x, y=y, button=action["button"].split(".")[-1])
        elif action["type"] == "mouse_move" and move_count < 5:
            x, y = action["position"]
            pyautogui.moveTo(x, y, duration=0.1)
            move_count += 1
        elif action["type"] == "key_press":
            pyautogui.press(action["key"].replace("'", ""))
        elif action["type"] == "wait":
            time.sleep(action["duration"])  # 执行等待
        elif action["type"] == "key_release":
            pass

    print("回放完成。")
    listener.stop()

if __name__ == "__main__":
    replay_actions()

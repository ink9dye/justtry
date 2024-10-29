import pyautogui
import time

# 操作序列，根据按键精灵录制内容生成
actions = [
    {"action": "move", "position": (292, 1173), "delay": 1029, "duration": 0.1},
    {"action": "left_down", "delay": 2},
    {"action": "left_down", "delay": 4},
    {"action": "left_down"},
    {"action": "move", "position": (1477, 1091), "delay": 2987, "duration": 0.1},
    {"action": "single_click"},
]

# 执行动作
for action in actions:
    # 处理延时
    if "delay" in action:
        time.sleep(action["delay"] / 1000.0)  # 毫秒转秒

    # 判断动作类型并执行
    if action["action"] == "move":
        x, y = action["position"]
        duration = action.get("duration", 0.1)  # 设置较小的 duration 以加快移动速度
        pyautogui.moveTo(x, y, duration=duration)
    elif action["action"] == "single_click":
        pyautogui.click()
    elif action["action"] == "left_down":
        pyautogui.mouseDown()

print("动作序列执行完毕。")

import pyautogui
from pynput import mouse

# 点击事件处理函数
def on_click(x, y, button, pressed):
    if pressed:  # 当鼠标按下时打印坐标
        print(f"Mouse clicked at ({x}, {y})")
        # 按下后可以在点击后暂停记录
        return False  # 停止监听

# 监听鼠标点击事件
print("请依次点击开始菜单、电源键和重启按钮。")
print("每次点击后都会记录坐标，并结束监听。")
print("重新运行脚本以记录下一个坐标。")

with mouse.Listener(on_click=on_click) as listener:
    listener.join()

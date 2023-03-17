# 地标和侧面实物采集及训练

import cv2
import numpy as np
import datetime
import time
import sys

sys.path.append("../")
from cart.widgets import Button

# 摄像头编号
# cam=0
cam = 1
# 程序开启运行开关
start_button = Button(1, "2")
# 程序关闭开关
stop_button = Button(1, "4")
camera = cv2.VideoCapture(cam)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
btn = 0
if __name__ == "__main__":
    if cam == 0:
        result_dir = "./front_image"
    # cam=1
    else:
        result_dir = "./side_image"
    print("Start!")
    print('''Press the "4 button" to take photos!''')
    while True:
        if stop_button.clicked():
            # 如果第四个按键被按下，则拍一张照片并存下
            print("btn", btn)
            path = "{}/{}.png".format(result_dir, btn)
            btn += 1
            time.sleep(0.2)
            return_value, image = camera.read()
            name = "{}.png".format(btn)
            cv2.imwrite(path, image)


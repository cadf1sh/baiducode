#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# 四个轮子的控制，电机驱动
import time
import serial
import sys
sys.path.append("../")
from config import CONTROLLER

# 77 68 0c 00 02 7a 01 01 32 02 33 03 32 04 33 0A
comma_head_01_motor = bytes.fromhex('77 68 06 00 02 0C 01 01')
comma_head_02_motor = bytes.fromhex('77 68 06 00 02 0C 01 02')
comma_head_03_motor = bytes.fromhex('77 68 06 00 02 0C 01 03')
comma_head_04_motor = bytes.fromhex('77 68 06 00 02 0C 01 04')
comma_head_all_motor = bytes.fromhex('77 68 0c 00 02 7a 01')
#                                                        01:一号板
comma_trail = bytes.fromhex('0A')


def speed_limit(speeds):
    i = 0
    for speed in speeds:
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100
        speeds[i] = speed
        i = i + 1
    return speeds


class Chassis:
    """
    底盘控制
    """

    def __init__(self):
        """
        :rtype: object
        """
        self.speed = 20
        self.kx = 0.85
        portx = "/dev/ttyUSB0"
        if CONTROLLER == "mc601":
            bps = 380400
        elif CONTROLLER == "wobot":
            bps = 115200
        else:
            bps = 115200
        self.serial = serial.Serial(portx, int(bps), timeout=0.000005, parity=serial.PARITY_NONE, stopbits=1)
        self.p = 0.8
        self.slow_ratio = 0.97
        self.min_speed = 20
    #  设置speed，只会影响到拐弯的时候的速度，正常驱动时，采用run函数重新给速度

    def steer(self, angle):
        print(angle)
        speed = int(self.speed)
        delta = angle * self.kx
        left_wheel = speed
        right_wheel = speed
    
        if delta < 0:
            left_wheel = int((1 + delta) * speed)
        else:
            right_wheel = int((1 - delta) * speed)
        print(delta)
        print("left_speed:", left_wheel, "  right_speed:", right_wheel)
        self.move([left_wheel, right_wheel, left_wheel, right_wheel])

    def stop(self):
        self.move([0, 0, 0, 0])

    def move(self, speeds):
        left_front = int(speeds[0])
        right_front = -int(speeds[1])
        left_rear = int(speeds[2])
        right_rear = -int(speeds[3])
        self.min_speed = int(min(speeds))
        # print(speeds)
        left_front_kl = bytes.fromhex('01') + left_front.to_bytes(1, byteorder='big', signed=True)
        right_front_kl = bytes.fromhex('02') + right_front.to_bytes(1, byteorder='big', signed=True)
        left_rear_kl = bytes.fromhex('03') + left_rear.to_bytes(1, byteorder='big', signed=True)
        right_rear_kl = bytes.fromhex('04') + right_rear.to_bytes(1, byteorder='big', signed=True)
        send_data_all_motor = (comma_head_all_motor + left_front_kl + right_front_kl + left_rear_kl + right_rear_kl
                               + comma_trail)
        self.serial.write(send_data_all_motor)
        time.sleep(0.001)

    def turn_left(self):
        speed = self.speed
        left_wheel = -speed
        right_wheel = speed
        self.move([left_wheel, right_wheel, left_wheel, right_wheel])

    def turn_right(self):
        speed = self.speed
        left_wheel = speed
        right_wheel = -speed

        self.move([left_wheel, right_wheel, left_wheel, right_wheel])

    def reverse(self):
        speed = self.speed
        self.move([-speed, -speed, -speed, -speed])


def test():
    c = Chassis()
    while True:
        c.move([50, 0, 50, 0])
        time.sleep(4)
        c.stop()
        time.sleep(1)


if __name__ == "__main__":
    speeds = [20, 19, 20, 19]
    c = Chassis()
    c.move(speeds)
    time.sleep(2)
    c.stop()
    # c.move([20, 20, 20, 20])
    # time.sleep(1)
    # c.run([0, 0, 0, 0])
    # time.sleep(1)
    # c.run([-20, -20, -20, -20])
    # time.sleep(1)
    # c.run([0, 0, 0, 0])
    # c.run([40,40,40,40])
    # time.sleep(1)
    # c.run([60,60,60,60])
    # time.sleep(1)
    # c.run([0, 0, 0, 0])

    # c = Cart()
    # while True:
    #     # c.run([5,5,5,5])
    #     c.run([10, 10, 10, 10])
    #     time.sleep(3)
    #     c.run([0, 0, 0, 0])
    #     time.sleep(3)

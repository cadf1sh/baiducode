#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 导入当前目录下的文件夹作为路径
import set_path
from cart.widgets import *
import time

def task_init():
    motor = Motor_rotate(2, 1)
    removemotor = Motor_rotate(2, 2)
    limit_switch = LimitSwitch(4)
    servo_grasp = Servo_pwm(2)
    magsens = Magneto_sensor(3)
    servo_grasp.servo_control(180, 70)
    print("aaaaaa")
    # time.sleep(2)
    motor.motor_rotate(80)
    time.sleep(1)
    motor.motor_rotate(0)
    kl = limit_switch.clicked()
    removemotor.motor_rotate(-60)
    while True:
        kl = limit_switch.clicked()
        if kl:
            time.sleep(0.05)
            removemotor.motor_rotate(0)
            break
    time.sleep(0.5)
    
def light_work(light_port, color, tim_t):
    light = Light(light_port)
    red = [80, 0, 0]
    green = [0, 80, 0]
    yellow = [80, 80, 0]
    off = [0, 0, 0]
    light_color = [0, 0, 0]
    if color == 'red':
        light_color = red
    elif color == 'green':
        light_color = green
    elif color == 'yellow':
        light_color = yellow
    elif color == 'off':
        light_color = off
    light.light_control(0, light_color[0], light_color[1], light_color[2])
    time.sleep(tim_t)
    light.light_off()


def purchase_good():
    motor = Motor_rotate(2, 1)
    removemotor = Motor_rotate(2, 2)
    limit_switch = LimitSwitch(4)
    servo_grasp = Servo_pwm(2)
    magsens = Magneto_sensor(3)
    servo_grasp.servo_control(90, 70)
    removemotor.motor_rotate(80)
    while True:
        kl = magsens.read()
        # print("kl=", kl, "\n")
        if kl != None and kl >= 70:
            removemotor.motor_rotate(0)
            break
    time.sleep(0.8)
    motor.motor_rotate(-50)
    time.sleep(1)
    motor.motor_rotate(0)
    servo_grasp.servo_control(180, 70)
    print("bbbbbb")
    time.sleep(1)
    removemotor.motor_rotate(90)
    time.sleep(1.8)
    removemotor.motor_rotate(0)
    # 收回
    motor.motor_rotate(80)
    time.sleep(1)
    motor.motor_rotate(0)
    # 购物完成后下降
    time.sleep(0.5)
    removemotor.motor_rotate(-80)
    while True:
        kl = magsens.read()
        # print("kl=", kl, "\n")
        if kl != None and kl >= 70:
            motor.motor_rotate(80)
            time.sleep(0.8)
            removemotor.motor_rotate(0)
            motor.motor_rotate(0)
            break
    


def raise_flag(servoID, light_port, flagname):
    print("raise_flag start!")
    servo_raise = Servo(servoID)
    # noflag
    # servo_raise.servo_control(42,60)
    # time.sleep(2)
    if flagname == "dunhuang":
        # dunhuang
        servo_raise.servo_control(-40, 60)
        time.sleep(1)
        for i in range(0, 3):
            light_work(light_port, "green", 0.1)
    elif flagname == "jsddb":
        # jsddb
        servo_raise.servo_control(-120, 60)
        time.sleep(1)
        for i in range(0, 3):
            light_work(light_port, "green", 0.1)
    elif flagname == "alamutu":
        # almutu
        servo_raise.servo_control(122, 60)
        time.sleep(1)
        for i in range(0, 3):
            light_work(light_port, "green", 0.1)
    # noflag
    servo_raise.servo_control(42, 60)
    # time.sleep(2)
    print("raise_flag stop!")


def shot_target():
    print("shot_target start!")
    servo_shot = Servo_pwm(1)
    removemotor = Motor_rotate(2, 2)
    time.sleep(0.5)
    servo_shot.servo_control(30, 80)
    print("cccccc")
    time.sleep(2)
    servo_shot.servo_control(160, 80)
    print("dddddd")
    time.sleep(0.5)
    print("shot_target stop!")


def shot_target2():
    print("shot_target start!")
    servo_shot = Servo_pwm(1)
    removemotor = Motor_rotate(2, 2)
    magsens = Magneto_sensor(3)
    limit_switch = LimitSwitch(4)
    time.sleep(0.5)
    removemotor.motor_rotate(60)
    while True:
        kl = magsens.read()
        print("kl=", kl, "\n")
        if kl != None and kl >= 70:
            time.sleep(0.8)
            removemotor.motor_rotate(0)
            break
    time.sleep(0.5)
    servo_shot.servo_control(30, 80)
    print("cccccc")
    time.sleep(2)
    servo_shot.servo_control(160, 80)
    print("dddddd")
    time.sleep(0.5)
    removemotor.motor_rotate(-60)
    time.sleep(1.0)
    removemotor.motor_rotate(0)
    print("shot_target stop!")


def trade_good_1():
    motor = Motor_rotate(2, 1)
    removemotor = Motor_rotate(2, 2)
    limit_switch = LimitSwitch(2)
    servo_grasp = Servo_pwm(2)
    magsens = Magneto_sensor(3)
    # 稍伸抓手
    motor.motor_rotate(-50)
    time.sleep(1.0)
    motor.motor_rotate(0)
    # 张开手抓
    servo_grasp.servo_control(50, 70)
    time.sleep(1.0)
    # 收回抓手
    motor.motor_rotate(50)
    time.sleep(0.8)
    motor.motor_rotate(0)
    servo_grasp.servo_control(0, 70)
    time.sleep(1.0)


def trade_good_2():
    motor = Motor_rotate(2, 1)
    traverse_motor = Motor_rotate(2, 2)
    limit_switch = LimitSwitch(2)
    servo_grasp = Servo_pwm(2)
    mag_sens = Magneto_sensor(3)
    # 上升
    traverse_motor.motor_rotate(60)
    time.sleep(1.0)
    while True:
        kh = mag_sens.read()
        print("kh=", kh, "\n")
        if kh >= 74:
            time.sleep(1.3)
            traverse_motor.motor_rotate(0)
            break
    motor.motor_rotate(-50)
    time.sleep(1.2)
    motor.motor_rotate(0)
    time.sleep(1)
    servo_grasp.servo_control(160, 70)
    time.sleep(0.8)
    traverse_motor.motor_rotate(60)
    time.sleep(0.3)
    traverse_motor.motor_rotate(0)
    motor.motor_rotate(50)
    time.sleep(0.8)
    motor.motor_rotate(0)


def trade_good():
    motor = Motor_rotate(2, 1)
    traverse_motor = Motor_rotate(2, 2)
    limit_switch = LimitSwitch(2)
    servo_grasp = Servo_pwm(2)
    mag_sens = Magneto_sensor(3)
    ultrasonic = UltrasonicSensor(4)
    # go
    while True:
        distance = ultrasonic.read()
        if distance != None and distance < 10:
            print("---------------------->")
            motor.motor_rotate(50)
            time.sleep(0.5)
            motor.motor_rotate(0)
            time.sleep(0.5)
            servo_grasp.servo_control(50, 70)
            time.sleep(0.5)
            servo_grasp.servo_control(160, 70)
            time.sleep(0.5)
            motor.motor_rotate(-50)
            time.sleep(0.5)
            motor.motor_rotate(0)
            # 张开手抓
            servo_grasp.servo_control(50, 70)
            time.sleep(0.5)
            break
    # 下降定位
    traverse_motor.motor_rotate(-60)
    while True:
        kl = mag_sens.read()
        print("kl=", kl, "\n")
        if kl >= 93:
            time.sleep(0.8)
            traverse_motor.motor_rotate(0)
            break
    traverse_motor.motor_rotate(60)
    time.sleep(1.5)
    while True:
        kh = mag_sens.read()
        print("kh=", kh, "\n")
        if kh >= 94:
            time.sleep(0.8)
            traverse_motor.motor_rotate(0)
            break
    motor.motor_rotate(50)
    time.sleep(0.3)
    motor.motor_rotate(0)
    time.sleep(1)
    servo_grasp.servo_control(160, 70)
    motor.motor_rotate(-50)
    time.sleep(0.5)
    motor.motor_rotate(0)
    traverse_motor.motor_rotate(-60)
    time.sleep(1)
    # 下降归位
    while True:
        kw = limit_switch.clicked()
        if kw:
            time.sleep(0.05)
            traverse_motor.motor_rotate(0)
            break


def buzzer():
    buzzer = Buzzer()
    for i in range(1, 10):
        # print(i)
        buzzer.rings()
        time.sleep(0.5)


if __name__ == '__main__':
    task_init()
    purchase_good()
    # time.sleep(0.5)
    # trade_good_1()
    # trade_good_2()
    # shot_target()
    # purchase_good()
    # trade_good()
    # raise_flag(2, 3, "dunhuang")  
    # time.sleep(1)
    # raise_flag(2, 3, "alamutu")
    # time.sleep(1)
    # raise_flag(2,3,"jsddb")
    # while True:
    #     light_work(3,"green",0.2)

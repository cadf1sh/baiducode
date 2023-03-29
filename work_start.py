#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from config import *
# 导入路径
import set_path
from cart.widgets import *
from cart.driver import Driver
from camera import Camera
from detector.detectors import *
from task_func import *

、


front_camera = Camera(FRONT_CAM, [640, 480])
side_camera = Camera(SIDE_CAM, [640, 480])
driver = Driver()

# 边界底边检测的类
cruiser = Cruiser()

# 地面标志检测
sign_detector = SignDetector()
# 侧边目标物检测
task_detector = TaskDetector()

# 程序开启运行开关
start_button = Button_angel(1, "2")
# 程序关闭开关
stop_button = Button_angel(1, "4")

# 设置舵机
servo1 = Servo(1)
servo2 = Servo(2)

task_9_flag = False

STATE_IDLE = "idle"
STATE_CRUISE = "cruise"
STATE_LOCATE_TASK = "sign_detected"
STATE_DO_TASK = "task"

sign_list = [0] * 11
order_num = 1
cam_dir = 1 # 左边为-1，右边为1


# 确认"4"按键是否按下，程序是否处于等待状态
def check_stop():
    if stop_button.clicked():
        return True
    return False


# 任务程序开始按钮检测函数
def idle_handler(params=None):
    driver.stop()
    global order_num
    order_num = 1
    while True:
        if start_button.clicked():
            print("program start!")
            # 调用到巡航模式
            return STATE_CRUISE, None
        time.sleep(0.4)
        print("IDLE")


# 按照给定速度沿着道路前进给定的时间
def lane_time(speed, my_time):
    start_time = time.time()
    driver.set_speed(speed)
    while True:
        if check_stop():
            return STATE_IDLE, None
        front_image = front_camera.read()
        error = cruiser.infer_cnn(front_image)
        driver.steer(error)
        timeout = time.time()
        if timeout - start_time > my_time:
            driver.stop()
            break


# 巡航模式
def cruise_handler(params=None):
    global order_num
    global sign_list
    global cam_dir

    # 设置小车巡航速度
    driver.set_speed(FULL_SPEED)
    # task: 二维字典
    # task[order_num]:一维的字典
    # task[order_num]['angle']:一维字典的值

    #控制舵机1转到任务order_num的角度
    servo1.servo_control(task[order_num]['angle'], 50)

    print(task[order_num]['angle'])

    if task[order_num]['angle'] > 45:
        cam_dir = -1
    else:
        cam_dir = 1

    lane_time(30, 3)
    driver.set_speed(50)
    while True:
        if check_stop():
            return STATE_IDLE, None
        front_image = front_camera.read()

        angle = cruiser.infer_cnn(front_image)

        # 根据图像预测的角度，使得车旋转一定的角度
        driver.steer(angle)

        # 侦测车道上有无标志图标
        res = sign_detector.detect(front_image)
        if len(res) != 0:
            print(res)
            # order_num:当前执行到的任务序列
            for sign in res:
                if sign.index == task[order_num]['sign']:

                    # 获取标志识别结果，获得所在列表的索引值
                    sign_list[sign.index] += 1
                    # 连续检测到一定次数，认为检测到，进入到任务定位程序
                    if sign_list[sign.index] > REC_NUM:
                        print('*****', res, '*****')
                        
                        return STATE_LOCATE_TASK, order_num

        else:
            sign_list = [0] * 6

# 标志位置测试
def sign_detecte_test():
    while True:
        front_image = front_camera.read()
        res_front = sign_detector.detect(front_image)
        if len(res_front) > 0:
            print(res_front)
            time.sleep(1)

# 任务位置测试
def task_detecte_test():
    while True:

        side_image = side_camera.read()
        res_side = task_detector.detect(side_image)
        if len(res_side) > 0:
            print(res_side)
            time.sleep(1)
            
# 当从巡航模式转换到做任务模式时，首先进行准确的位置定位，本函数即实现以上功能。后面进行做任务。
def locate_task_handler(params= None):
    global order_num
    global cam_dir
    print("params is",params)
    order_num += 1
    driver.set_speed(SLOW_SPEED)
    start_time = time.time()
    
    front_image = front_camera.read()
    angle = cruiser.infer_cnn(front_image)
    # driver.steer(angle)

    side_image = side_camera.read()
    res_side = task_detector.detect(side_image)
    _x, _y = 500, 500
    # 检测到位置有停下
    while True:
        if check_stop():
            return STATE_IDLE, None

        # 侧面确实是识别到了有效信息
        if len(res_side) > 0:
            for res in res_side:
                if res.index in task[params]['index']:
                    # 标签到一定位置退出循环

                    task_functions[res.index]['position']
                    # res: 识别到的内容，最起码包括识别的类型和识别到的点的坐标
                    # _x,_y:小车在运行过程中实时识别的中心点坐标和，已知的准确位置下该类型的中心点坐标之间的差
                    _x, _y = res.error_from_point(task_functions[res.index]['position'])

                    print(cam_dir)
                    # 确认方向
                    _x = _x * cam_dir
                    print(_x)
                    # 做一些设置吧
                    if _x > -20:
                        if task[params]['location'] == False:
                            return STATE_DO_TASK, res.index
                        break
                    elif _x > -100:
                        driver.set_speed(10)
            if _x > -20:
                if task[params]['location'] == False:
                    return STATE_DO_TASK, res.index
                print("location")
                break
        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > LOCATE_TIME:
            return STATE_CRUISE, None

        # 开始准备做任务
        front_image = front_camera.read()
        angle = cruiser.infer_cnn(front_image)
        # 1.调整位置
        driver.steer(angle)
        # res_front = sign_detector.detect(front_image)
        # 2.再获取一帧准确的图像
        side_image = side_camera.read()
        res_side = task_detector.detect(side_image)

    
    while True:
        if check_stop():
            return STATE_IDLE, None
        if len(res_side) > 0:
            for res in res_side:
                if res.index in task[params]['index']:
                    # 标签到一定位置退出循环
                    _x, _y = res.error_from_point(task_functions[res.index]['position'])
                    _x = _x * cam_dir
                    print(_x)
                    # 控制左右行走
                    if _x < -20:
                        pass
                        driver.run(10, 10)
                    elif _x > 20:
                        pass
                        driver.run(-10, -10)
                    else:
                        # 定位成功
                        driver.stop()
                        print("location ok")
                        return STATE_DO_TASK, res.index

        current_time = time.time()
        # 长时间未到达位置
        if current_time - start_time > LOCATE_TIME:
            return STATE_CRUISE, None
        side_image = side_camera.read()
        res_side = task_detector.detect(side_image)
    


# 做任务
def do_task_handler(params=None):
    print("*******", "now do task:", str(params), TASK_LABEL[params], "*******")
    global task_9_flag

    if params == 1:     # alamutu
        raise_flag(2, 3, "alamutu")

    elif params == 2:   # bad_person
        driver.run(-13, -12)
        time.sleep(1.2)
        driver.stop()
        shot_target()

    elif params == 3:   # bad_person
        driver.run(-13, -11)
        time.sleep(1.4)
        driver.stop()
        shot_target2()

    elif params == 4:   # dunhuang
        driver.run(10, 10)
        time.sleep(0.7)
        driver.stop()
        raise_flag(2, 3, "dunhuang")

    elif params == 5:   # friendship
        timein = time.time()
        cur_speed = driver.full_speed
        driver.set_speed(cur_speed)
        while True:
            timeout = time.time()
            if check_stop():
                return STATE_IDLE, None
            front_image = front_camera.read()
            driver.run(front_image)
            if timeout - timein > 1.2:
                driver.stop()
                break
        driver.run(13, -13)
        time.sleep(1.5)
        driver.run(-13, -13)
        time.sleep(2.4)
        driver.stop()
        time.sleep(2.0)
        driver.run(9, 20)
        time.sleep(2.8)
        driver.stop()

    elif params == 6:   # goodperson
        pass

    elif params == 7:   # goodperson
        pass

    elif params == 8:   # jstdb
        driver.run(-13, -13)
        time.sleep(0.7)
        driver.stop()
        raise_flag(2, 3, "jstdb")

    elif params == 9:   # purchase
        purchase_good()


    elif params == 10:   # trade
        # 调试
        if not task_9_flag:
            task_9_flag = True
            driver.run(-13, -13)
            time.sleep(1.8)
            driver.stop()
            trade_good_1()
            driver.run(-13, -13)
            time.sleep(1.8)
            driver.stop()
            return STATE_DO_TASK, params
        else:
            driver.run(-13, -13)
            time.sleep(0.3)
            driver.stop()
            trade_good_2()

    return STATE_CRUISE, None


state_map = {
    STATE_IDLE: idle_handler,
    STATE_CRUISE: cruise_handler,
    STATE_LOCATE_TASK: locate_task_handler,
    STATE_DO_TASK: do_task_handler,
}

if __name__ == '__main__':
    front_camera.start()
    side_camera.start()
    # 基准速度
    driver.set_speed(40)

    # 120，左；-50，右；
    # servo1.servo_control(-45, 50)
    # servo1.servo_control(120, 50)
    # sign_detecte_test()
    # task_detecte_test()
    time.sleep(2)
    current_state = STATE_IDLE
    arg = "cruise"

    startmachine()
    task_init()
    # 延时
    time.sleep(0.2)
    
    while True:
        pass
    try:
        while True:
            current_state, arg = state_map[current_state](arg)
    except ZeroDivisionError as e:
        print('except:', e)
        driver.stop()
        front_camera.stop()
        side_camera.stop()
    finally:
        print('finally...')
        driver.stop()
        front_camera.stop()
        side_camera.stop()
    
    '''
    params = None
    idle_handler()
    order_num = 3
    _, params = cruise_handler(params)
    _, params = locate_task_handler(params)
    driver.stop()
    front_camera.stop()
    side_camera.stop()
    '''


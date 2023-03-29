#!/usr/bin/python3
# -*- coding: utf-8 -*-

FRONT_CAM = 0   # 前摄像头编号
SIDE_CAM = 1    # 边摄像头编号
#                                              sign:大概是地面的标号？不清楚      index:?啥含义啊
task = {
        1:{"label":"采购货物", "angle":-50, "location":True, "sign":4, "index":[9]},
        2:{"label":"文化交流", "angle":125, "location":False, "sign":1, "index":[1, 4, 8]},
        3:{"label":"守护丝路", "angle":125, "location":True, "sign":3, "index":[2, 3, 6, 7]},
        4:{"label":"守护丝路", "angle":125, "location":False, "sign":3, "index":[2, 3, 6, 7]},
        5:{"label":"放歌友谊", "angle":125, "location":False, "sign":2, "index":[5]},
        6:{"label":"守护丝路", "angle":125, "location":False, "sign":3, "index":[2, 3, 6, 7],},
        7:{"label":"文化交流", "angle":125, "location":False, "sign":1, "index":[1, 4, 8], },
        0:{"label":"翻山越岭", "angle":125, "location":False, "sign":0,"index":[],},
        8:{"label":"文化交流", "angle":125, "location":False, "sign":1, "index":[1, 4, 8],},
        9:{"label":"以物易物", "angle":-50, "location":True, "sign":5, "index":[10]},
        10:{"label":"守护丝路", "angle":-50, "location":False, "sign":3,"index":[2, 3, 6, 7]},
        }
task_functions = {
                1:{"label":"阿拉木图","position":[155,340]}, # 位置7
                2:{"label":"坏人1","position":[5, 158]}, # 位置10
                3:{"label":"坏人2","position":[615, 158]}, # 位置3
                4:{"label":"敦煌","position":[480,340]},  # 位置2
                5:{"label":"放歌友谊","position":[]},   #位置5
                6:{"label":"好人1","position":[615, 250]},    # 位置4
                7:{"label":"好人2","position":[615, 250]},    # 位置6
                8:{"label":"君士坦丁堡","position":[480, 340]},  # 位置8
                9:{"label":"采购货物","position":[135,340]},    # 位置1
                10:{"label":"以货易货","position":[]},  # 位置9
                }
CONTROLLER = "mc601"
# CONTROLLER = "wobot"


REC_NUM = 2     # 图标出现次数而统计确认识别结果

POSITION_THRESHOLD = 10     # 位置偏差阈值

HIGH_SPEED = 40         # 高速速度
FULL_SPEED = 20         # 中速速度
SLOW_SPEED = 16         # 慢速速度，加速速度
ACCELERATION_TIME = 3   # 启动时间

SIGN_LOCATE_TIME = 1.4
LOCATE_TIME = 100

sign_label = {"background": 1, "castle": 1, "friendship": 1, "guard": 1, "purchase": 1, "trade": 1}
TASK_LIST = []
TASK_LABEL = ["background", "alamutu", "badperson", "badperson2", "dunhuang", "friendship", "goodperson", "goodperson2", "jstdb", "purchase", "trade"]

# coding:utf-8
import cv2
import sys
import time


# time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
#cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
time.sleep(1)
frame = cv2.imread("side_image/290.png")

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test_wang.avi', fourcc, 6, (640, 480))
time.sleep(1)
print(2)
count = 0
while True:
    ret = True
    #,frame = cap.read()
    count += 1
    
    if ret == True:
        print(count)
        if count > 100:
            break
        # cv2.imwriter()
        # cv2.imshow("test",frame)
        a = out.write(frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    else:
        break
    cv2.waitKey(1)
print("exit")
# cap.release()
out.release()
# cv2.destroyAllWindows()

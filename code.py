import numpy as np
import cv2
from time import *
from RPi.GPIO import *
setmode(BCM)
setup(6,OUT)
setup(13,OUT)
setup(15,OUT)
setup(26,OUT)

t=time()

m1=PWM(6,50)
m1.start(0)
m2=PWM(13,50)
m2.start(0)
m3=PWM(15,50)
m3.start(0)
m4=PWM(26,50)
m4.start(0)
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)

try:
    while True:
        ret, frame = cap.read()
        low_b = np.uint8([70,70,70])
        high_b = np.uint8([0,0,0])
        mask = cv2.inRange(frame, high_b, low_b)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        try:
            c = max(contours, key=cv2.contourArea)
        except:
            pass
        M = cv2.moments(c)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print(M['m00'])
            #print("CX : "+str(cx)+"  CY : "+str(cy))

            if cx >= 120 : #поворот налево
                m2.ChangeDutyCycle(10)
                m4.ChangeDutyCycle(5)
                m1.ChangeDutyCycle(10)
                m3.ChangeDutyCycle(10)
            if cx < 120 and cx > 40 : #едем прямо
                m2.ChangeDutyCycle(5)
                m4.ChangeDutyCycle(10)
                m1.ChangeDutyCycle(10)
                m3.ChangeDutyCycle(10)
            if cx <=40 : #поворот направо
                m2.ChangeDutyCycle(5)
                m4.ChangeDutyCycle(10)
                m1.ChangeDutyCycle(5)
                m3.ChangeDutyCycle(5)

        if time()-t>5:
            cv2.drawContours(frame, c, -1, (0,255,0), 1)
            cv2.imshow("Mask",mask)
            cv2.imshow("frame",frame)
except KeyboardInterrupt:
    print("sddsgs")
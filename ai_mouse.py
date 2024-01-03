import sys

import cv2
from cvzone.HandTrackingModule import HandDetector
import macmouse as mouse
import numpy as np
import pyautogui
import time


CLIK = False
clik_time = 0
DRAG = False
drag_time = 0

pTime = 0


def get_clik_lock(now):
    global clik_time
    if clik_time == 0 and CLIK ==False:
        #initial clik time setting
        clik_time = now
        return True
    elif now - clik_time > 1:
        #proper clik time
        clik_time = now
        return True
    elif now - clik_time < 1:
        #maybe repeatitive clik ban
        return False
    
def get_drag_lock(now):
    global drag_time
    if drag_time == 0 and DRAG ==False:
        drag_time = now
        return True
    elif now - drag_time > 1:
        drag_time = now
        return True
    elif now - drag_time < 1:
        return False
    

max_camera_number = 10

for cam_number in range(0,max_camera_number):
    cap = cv2.VideoCapture(cam_number)
    if cap.isOpened():
        print(f"Camera({cam_number}) load success")
        break
    elif cam_number == max_camera_number-1:
        sys.exit("Error: we cannot find usable camera.")
   
screen_width, screen_height = pyautogui.size()

cam_width, cam_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))     
        
# 비디오 프레임 크기, 전체 프레임수, FPS 등 출력
print('Frame width:', int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print('Frame height:', int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('Frame count:', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

fps = cap.get(cv2.CAP_PROP_FPS)
print('FPS:', fps)

frameR = 50

#cam_w, cam_h = 640, 480
#cap.set(3, cam_w)
#cap.set(4, cam_h)

detector = HandDetector(detectionCon=0.9, maxHands=1)

while True:
    
    success, img = cap.read()   #camera에서 가져온 프레임 단위의 단순 이미지
    img = cv2.flip(img, 1)      #1: 좌우반전, 2: 상하반전
    
    hands, img = detector.findHands(img, flipType=False)        #detector를 이용해서 hand를 찾은 결과를 return. img가 손에 대해 gesture detection 결과를 마킹 한 이미지임.
    
    cv2.rectangle(img, (frameR, frameR), (cam_width-frameR, cam_height-frameR), (255,0,255), 2)
    
    if hands:
        lmlist = hands[0]["lmList"]
        ind_x, ind_y = lmlist[8][0], lmlist[8][1]
        
        ind_x_3, ind_y_3 = lmlist[12][0], lmlist[12][1]
        ind_x_1, ind_y_1 = lmlist[4][0], lmlist[4][1]
        
        
        length, info, img = detector.findDistance((ind_x, ind_y), (ind_x_3, ind_y_3), img=img)
        
        if length < 60:
            if DRAG == False and get_drag_lock(time.time()) == True:
                DRAG = True
            elif DRAG == True and get_drag_lock(time.time()) == True:
                DRAG = False
                
        length, info, img = detector.findDistance((ind_x, ind_y), (ind_x_1, ind_y_1), img=img)
        
        if length < 60:
            if CLIK == False and get_clik_lock(time.time()) == True:
                CLIK = True
            elif CLIK == False and get_clik_lock(time.time())==True:
                CLIK = False
        
        
        cv2.circle(img, (ind_x, ind_y), 5, (0,255,255), 2)
        
        fingers = detector.fingersUp(hands[0])
        
        if fingers[1] == 1:
            conv_x = np.interp(ind_x, (frameR, cam_width-frameR), (0, screen_width))
            conv_y = np.interp(ind_y, (frameR, cam_height-frameR), (0, screen_height))
            
            
            if fingers[2] == 1 and DRAG == True:
                pyautogui.dragTo(conv_x, conv_y, button="left")
            elif CLIK == True:
                #pyautogui.click()
                pyautogui.doubleClick()
                CLIK = False
                print("double clik")
            else:
                pyautogui.moveTo(conv_x, conv_y)
                
    
    cTime = time.time()
    fps = int(1/(pTime-cTime))
    pTime = cTime
    cv2.putText(img, str(fps), (20,50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255,0,0), 3)            
        
    
    cv2.imshow("Camera fead", img)
    cv2.waitKey(1)
import cv2
from cvzone.HandTrackingModule import HandDetector

from virtual_mouse.video import get_ip_webcam, get_pc_webcam
from virtual_mouse.finger import get_hands, get_finger_position
from virtual_mouse.bounding_box import get_valid_box

import sys
import numpy as np
import pyautogui
import time


MOVING = False
CLIK_RANGE = 10
#pyautogui.FAILSAFE = False
screen_margin = 1

#0. constant setting
frameR_hegith = 100
frameR_width = 350


frameR_hegith_top = 300
frameR_hegith_bottom = 100


smooth = 10

max_handas_number = 1
detection_confidence = 0.9 #0~1.0
screen_width, screen_height = pyautogui.size()

detector = HandDetector(detectionCon=detection_confidence, maxHands=max_handas_number)

cap = get_pc_webcam()

cam_width, cam_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  

#cam_width -= screen_margin
#cam_height -= screen_margin


hand_number = 0


while True:
    success, img = cap.read()   #camera에서 가져온 프레임 단위의 단순 이미지
    img = cv2.flip(img, 1)      #1: 좌우반전, 2: 상하반전
    
       
    cv2.rectangle(img, (frameR_width, frameR_hegith_top), (cam_width-frameR_width, cam_height-frameR_hegith_bottom), (255,0,255), 2)
    
    if success:
        hands, img = detector.findHands(img, flipType=False)   
    else:
        pass
    
    
    if hands:
        hand1 = hands[0]
        bbox1 = hand1["bbox"]
        lmlist = hand1["lmList"]
        
        x, y, w, h = bbox1
        
        #thumb_x, thumb_y = get_finger_position(hands=hands, hand_number=hand_number, finger_name="thumb")
        #index_x, index_y = get_finger_position(hands=hands, hand_number=hand_number, finger_name="index")
        thumb_x, thumb_y = lmlist[4][0], lmlist[4][1]
        index_tip_x, index_tip_y = lmlist[8][0], lmlist[8][1]
        index_x, index_y = lmlist[5][0], lmlist[5][1]
        
        #4. Interprete into screen size
        #now_x, now_y = pyautogui.position()
        
        conv_x = np.interp(index_x, (frameR_width, cam_width-frameR_width), (0, screen_width))
        conv_y = np.interp(index_y, (frameR_hegith_top, cam_height-frameR_hegith_bottom), (0, screen_height))
        
        
        fingers = detector.fingersUp(hands[0])
        
        if fingers[1]==1:
            distance = detector.findDistance((thumb_x, thumb_y), (index_x, index_y))[0]
            print(distance)
            
            if distance < CLIK_RANGE:
                try:
                    pyautogui.click(x=conv_x, y=conv_y, button='left')
                    print("left clik", time.time())
                    pyautogui.sleep(0.1)
                except:
                    print("Corner error", conv_x, conv_y)
            elif fingers[2]==1:
                try:
                    pyautogui.click(x=conv_x, y=conv_y, button="right")
                    print("right clik", time.time())
                    pyautogui.sleep(0.1)
                except:
                    print("Corner error", conv_x, conv_y)
            
            else:
            
                try:
                    pyautogui.moveTo(conv_x, conv_y)
                    
                except:
                    print("Corner error", conv_x, conv_y)
                
            print(fingers)
        
    
    #cv2.imshow("Camera fead", img)
    cv2.waitKey(1)
        
import cv2
from cvzone.HandTrackingModule import HandDetector

from virtual_mouse.video import get_ip_webcam, get_pc_webcam
from virtual_mouse.finger import get_hands, get_finger_position

import sys
import numpy as np
import pyautogui
import time

#0. constant setting
frameR_hegith = 300
frameR_width = 100
my_url = "http://10.8.0.217:8080"
max_handas_number = 1
detection_confidence = 0.9 #0~1.0
screen_width, screen_height = pyautogui.size()

detector = HandDetector(detectionCon=detection_confidence, maxHands=max_handas_number)


while True:
    
    #1. Get webcam image information using url.
    img = get_ip_webcam(user_url=my_url)   
    
    
    #2. Webcam screen setting for deciding the valid area. 
    cam_height, cam_width, _ = img.shape
    cv2.rectangle(img, (frameR_width, frameR_hegith), (cam_width-frameR_width, cam_height-frameR_hegith), (255,0,255), 2)
    
    #3. Find hands in the image.
    hands, img = detector.findHands(img, flipType=False)
    
    if hands:
        hand_number=0
        fingers = detector.fingersUp(hands[hand_number])
        
        thumb_x, thumb_y = get_finger_position(hands=hands, hand_number=hand_number, finger_name="index")
        
        cv2.circle(img=img, center=(thumb_x, thumb_y), radius=10, color=(255,0,255), thickness=3)
        
        #4. Interprete into screen size
        conv_x = np.interp(thumb_x, (frameR_width, cam_width-frameR_width), (0, screen_width))
        conv_y = np.interp(thumb_y, (frameR_hegith, cam_height-frameR_hegith), (0, screen_height))
        
        #5. Move mouse pointer to the point.
        
    
    #display webcam (optional)
    try:   
        cv2.imshow("webcam",img)
    
    except:
        sys.exit("Unable to connect to webcam check your smartphone please")
    
    if hands:
        pyautogui.moveTo(conv_x, conv_y, 0.01,pyautogui.easeInOutQuad)
        #pyautogui.sleep(0.1)
        
    if cv2.waitKey(1) == 27:
        break
    
    
#Weakness and disadvantage
#1. Cutting of mouse movement. It must move more smoothly.
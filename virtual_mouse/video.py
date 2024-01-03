# Import essential libraries 
import requests 
import cv2 
import numpy as np 
import imutils 
import sys

def get_pc_webcam(webcam_number=0, max_camera_number = 10):
    for cam_number in range(0,max_camera_number):
        cap = cv2.VideoCapture(cam_number)
        if cap.isOpened():
            print(f"Camera({cam_number}) load success")
            break
        elif cam_number == max_camera_number-1:
            sys.exit("Error: we cannot find usable camera.")
            
    
    return cap
    

def get_ip_webcam(user_url: str)->np.array:
    img_resp = requests.get(user_url+"/shot.jpg")
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=1000, height=1800) 
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.flip(img, 1)
    return img
    
"""
# Replace the below URL with your own. Make sure to add "/shot.jpg" at last. 
url = "http://192.168.106.122:8080/shot.jpg"

# While loop to continuously fetching data from the Url 
while True: 
    img_resp = requests.get(url) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    img = cv2.imdecode(img_arr, -1) 
    img = imutils.resize(img, width=1000, height=1800) 
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.flip(img, 1)
    cv2.imshow("Android_cam", img) 

	# Press Esc key to exit 
    if cv2.waitKey(1) == 27: 
        break
"""

cv2.destroyAllWindows() 

if __name__ == "__main__":
    
    user_url = "your_url"
    while True:
        webcam = get_ip_webcam(user_url=user_url)
        cv2.imshow(webcam)
        
    
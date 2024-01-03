from cvzone.HandTrackingModule import HandDetector
import numpy as np

detector = HandDetector(detectionCon=0.9, maxHands=1)

finger_dic = {"center": 0, "thumb":4, "index": 8, "middle": 12, "ring": 16, "litle": 20}


def get_hands(detector: HandDetector, img: np.array)->list:
    hands, img = detector.findHands(img, flipType=False)
    if hands:
        hands, img
    else:
        return None, None
    
def get_finger_position(hands: list, hand_number:int=0,finger_name: str="center")->tuple:
    finger_name = finger_name.lower()
    
    if finger_name not in finger_dic.keys():
        raise KeyError("Wrong finger name is passed. Check your finger name.")
    
    else:
        lmlist = hands[hand_number]["lmList"]
        x_pos, y_pos = lmlist[finger_dic[finger_name]][0], lmlist[finger_dic[finger_name]][1]
        return x_pos, y_pos    
    
def compute_fingers_distance(f1:tuple, f2:tuple)->int:
    if isinstance(f1, tuple) and isinstance(f2, tuple):
        f1_x, f1_y = f1
        f2_x, f2_y = f2
        distance = (np.sqrt(np.square(f1_x-f2_x)) + np.sqrt(np.square(f1_y-f2_y))) * 0.5
        return distance
    
    else:
        raise TypeError("Finger position must be a tuple type.")
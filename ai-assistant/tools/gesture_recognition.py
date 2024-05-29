import cv2
import time 
import numpy as np
from hand_tracker import HandTracker 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

w_cam, h_cam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, w_cam)
cap.set(4, h_cam)

# wrist -> 0
# thumb -> 1,2,3,4
# index -> 5,6,7,8
# middle -> 9,10,11,12
# ring -> 13,14,15,16
# pinky -> 17,18,19,20

tracker = HandTracker(detection_confidence=0.7)

class GestureRecognition:
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        self.volume_range = self.volume.GetVolumeRange()
        self.min_vol = self.volume_range[0]
        self.max_vol = self.volume_range[1]
        
    def control_volume(self,vol):
        # volume.GetMute()
        self.volume.SetMasterVolumeLevel(vol, None)

    def read_gesture(self):
        while True:
            success, img = cap.read()
            img = tracker.find_hands(img)
            lm_list = tracker.find_position(img,draw=False)

            if len(lm_list) != 0:
                x1, y1 = lm_list[4][1], lm_list[4][2]
                x2, y2 = lm_list[8][1], lm_list[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                length = np.hypot(x2 - x1, y2 - y1)
                vol = np.interp(length, [50, 300], [self.min_vol, self.max_vol])
                self.control_volume(vol)

            cv2.imshow("Image", img)
            cv2.waitKey(1)

        
if __name__ == "__main__":
    pass
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

tracker = HandTracker(detection_confidence=0.7, max_hands=1)

class GestureRecognition:
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        self.volume_range = self.volume.GetVolumeRange()
        self.min_vol = self.volume_range[0]
        self.max_vol = self.volume_range[1]
        self.min_brightness = 0
        self.max_brightness = 100
        
        
    def control_volume(self,length):
        # volume.GetMute()
        smoothness = 5
        vol_bar = np.interp(length, [50, 200], [self.min_vol, self.max_vol])
        vol_per = np.interp(length, [50, 200], [0, 100])
        vol_per = smoothness * round(vol_per/smoothness)
        self.volume.SetMasterVolumeLevelScalar(vol_per/100, None)
        
    def control_brightness(self,brightness):
        pass
    
    def read_gesture(self):
        while True:
            success, img = cap.read()
            img = tracker.find_hands(img)
            lm_list,bbox = tracker.find_position(img,draw=False)

            if len(lm_list) != 0:
                # Filter based on size
                wb, hb = bbox[2]-bbox[0], bbox[3]-bbox[1]
                area = wb*hb//100
                if 250 < area < 1000:
                    
                    # Find distance between thumb and index finger
                    length,img,_ = tracker.find_distance(4, 8, img, draw=False)
                    # Check fingers up
                    fingers = tracker.finger_up()                    
                    # if pinky down, set volume
                    if fingers[4] == 0:
                        print("Volume set")
                        self.control_volume(length)                   

            cv2.imshow("Image", img)
            cv2.waitKey(1)

        
if __name__ == "__main__":
    pass
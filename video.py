import cv2
import HandDetection as hd
import numpy as np
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv2.VideoCapture(0)
ptime = 0
detecter = hd.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volume_range = volume.GetVolumeRange()
# (-65.25, 0.0, 0.03125)
# minVol = -65.25. ie; volume[0]
# maxVol = 0.0. ie; volume[1]

minVol = volume_range[0]
maxVol = volume_range[1]

# volume.SetMasterVolumeLevel(0.0, None)


# FPS -> Frame per Seconds
while True:
    ret, frame = cap.read()

    detecter.findHands(frame)
    poshand=detecter.findPosition(frame, draw=False)
    if len(poshand) > 0:
        # print(poshand[8], poshand[4])
        x1, y1 = poshand[8][1], poshand[8][2]
        x2, y2 = poshand[4][1], poshand[4][2]

        mx, my = (x1+x2)//2, (y1+y2)//2

        cv2.circle(frame,(x1,y1),15,(255,0,0),cv2.FILLED)
        cv2.circle(frame,(x2,y2),15,(255,0,0),cv2.FILLED)
        cv2.line(frame,(x1,y1),(x2,y2),(0,0,0),3)
        cv2.circle(frame,(mx,my),15,(110,230,88),cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        # print(length)
        # hand range 190 to 30
        # vol range -65 to 0

        vol = np.interp(length, [30, 190], [minVol, maxVol])

        # print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length <= 30:
            cv2.circle(frame, (mx, my), 15, (0, 0, 255), cv2.FILLED)


    # fps code
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(frame, "FPS : "+str(int(fps)), (10,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("window", frame)
    #cv2.waitKey(1) # returns the ASCII values of the key pressed

    if cv2.waitKey(1) == ord('x'):
        break
    if cv2.waitKey(1) == ord('d'):
        cv2.imwrite("dance`1````````````````````````````````````````7.png",frame)
cap.release()
cv2.destroyAllWindows()

print("Thank You !!")

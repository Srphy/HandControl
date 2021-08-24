import cv2 as cv
import numpy as np
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640,480
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1, detectionCon=0.75)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv.circle(img, (x1, y1) ,7, (0, 255, 0), cv.FILLED)
        cv.circle(img, (x2, y2) ,7, (0, 255, 0), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (96, 215, 30), 2)
        cv.circle(img, (cx, cy) ,5, (0, 255, 0), cv.FILLED)

        lenght = math.hypot(x2-x1, y2-y1)
        print(int(lenght))
        vol = np.interp(lenght, [40,180], [(minVol +35), (maxVol-5)])
        volBar = np.interp(lenght, [40,180], [450, 150])
        volTxt = np.interp(lenght, [40,180], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)       

        if lenght < 45:
            cv.circle(img, (cx, cy) ,5, (0, 0, 255), cv.FILLED) 

        cv.rectangle(img, (30,150), (65,450), (96, 215, 30), 2, cv.LINE_AA)
        cv.rectangle(img, (30, int(volBar)), (65,450), (96, 215, 30), cv.FILLED, cv.LINE_AA)
        cv.putText(img, f'{int(volTxt)}%', (30, 475), cv.FONT_HERSHEY_DUPLEX, 1, (0, 215, 0), 1, cv.LINE_AA)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (5, 30), cv.FONT_HERSHEY_DUPLEX, 1, (96, 215, 30), 1, cv.LINE_AA)
    cv.imshow("Image", img)

    k = cv.waitKey(1)
    if k == 27:  # Esc key to breakloop and shutdown
        break

cv.destroyAllWindows()

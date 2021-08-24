import cv2 as cv
import numpy as np
import pynput as pn
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv.VideoCapture(0)
wCam, hCam = 1280, 720
cap.set(3, wCam)
cap.set(4, hCam)
detector = HandDetector(detectionCon=0.8)
opacity = 0.75
contourColor = 30, 255, 30
buttonColor = 100, 150, 100
buttonColor2 = 75, 150, 75
buttonColor3 = 75, 255, 75
finalText = ""
keyboard = Controller()
keys = [
    #["Es", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
    #["²", "&", "é", "\"", "\'", "(", "-", "è", "_", "ç", "à", ")", "=", "←"],
    [None, None, None, None, None,"A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"],
    [None, None, None, None, None,"Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
    [None, None, None, None, None,"W", "X", "C", "V", "B", "N", ",", ";", ":", "!"],
    [None, None, None, None, None," ", " ", " ", " ", " ", " ", " ", "1", "2", "3"],
    [None, None, None, None, None, None, None, None, None, None, None, None, "4", "5", "6"],
    [None, None, None, None, None, None, None, None, None, None, None, None, "7", "8", "9"]
]

def draw(img, buttonList):
    overlay = img.copy()
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        h2 = int(h/3)
        w2 = int(w/3)
        h3 = int(h/1.5)
        w3 = int(w/1.5)
         
        cv.rectangle(overlay, (button.pos), (x+w2, y+h2), contourColor, 4, cv.LINE_AA) # Top-left corner
        cv.rectangle(overlay, (x+w, y), (x+w3, y+h2), contourColor, 4, cv.LINE_AA) # Top-right corner
        cv.rectangle(overlay, (x+w, y+h), (x+w3, y+h3), contourColor, 4, cv.LINE_AA) # Bottom-right corner
        cv.rectangle(overlay, (x, y+h), (x+w2, y+h3), contourColor, 4, cv.LINE_AA) # Bottom-left corner
        cv.rectangle(overlay, button.pos, (x+w, y+h), buttonColor, cv.FILLED, cv.LINE_AA)
        cv.putText(overlay, button.text, (x + 18, y + 28), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv.LINE_AA)

        cv.rectangle(overlay, (150, 600), (165, 615), contourColor, 3, cv.LINE_AA) # Top-left corner
        cv.rectangle(overlay, (1130, 600), (1115, 615), contourColor, 4, cv.LINE_AA) # Top-right corner
        cv.rectangle(overlay, (1130, 650), (1115, 635), contourColor, 4, cv.LINE_AA) # Bottom-right corner
        cv.rectangle(overlay, (150, 650), (165, 635), contourColor, 4, cv.LINE_AA) # Bottom-left corner
        cv.rectangle(overlay, (150, 600), (1130, 650), buttonColor, cv.FILLED, cv.LINE_AA)
        cv.putText(overlay, finalText, (155, 635), cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1, cv.LINE_AA)

    cv.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
    return img

class Button():
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        if key != None:
            buttonList.append(Button([80*x + 55, 80 * i + 80], key))

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img, draw=False)
    img = draw(img, buttonList)

    if len(lmList) != 0:
        x2, y2 = lmList[8][0], lmList[8][1]
        cv.circle(img, (x2, y2) ,7, contourColor, cv.FILLED, cv.LINE_AA)

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x+w and y<lmList[8][1] < y + h:
                cv.rectangle(img, button.pos, (x+w, y+h), buttonColor2, cv.FILLED, cv.LINE_AA)
                cv.putText(img, button.text, (x + 18, y + 28), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv.LINE_AA)

                l,_,_ = detector.findDistance(8,12, img, draw=False)
                if l<30:
                    keyboard.press(button.text)
                    cv.rectangle(img, button.pos, (x+w, y+h), buttonColor3, cv.FILLED, cv.LINE_AA)
                    cv.putText(img, button.text, (x + 18, y + 28), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv.LINE_AA)
                    finalText += button.text
                    sleep(0.25)

    cv.imshow("Keyboard", img)
    k = cv.waitKey(1)
    if k == 27:  # Esc key to breakloop and shutdown
        break

cv.destroyAllWindows()

import cv2 as cv
import numpy as np
import matplotlib

img = cv.imread('cube.jpg')
overlay = img.copy()



cv.rectangle(overlay, (30,30), (150,150), (30, 255, 30), 7, cv.LINE_AA) # Top-left corner
cv.rectangle(overlay, (370,30), (250,150), (30, 255, 30), 7, cv.LINE_AA) # Top-right corner
cv.rectangle(overlay, (30,370), (150,250), (30, 255, 30), 7, cv.LINE_AA) # Bottom-left corner
cv.rectangle(overlay, (370,370), (250,250), (30, 255, 30), 7, cv.LINE_AA) # Bottom-right corner
cv.rectangle(overlay, (30,30), (370,370), (96, 215, 30), cv.FILLED, cv.LINE_AA)
#cv.rectangle(img, (30,30), (370,370), (96, 215, 30), cv.FILLED, cv.LINE_AA) # Green

#cv.putText(img, (30,30), (370,370), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2, cv.LINE_AA)
opacity = 0.75
cv.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)

while True:     
    cv.imshow("test", img)

    k = cv.waitKey(1)
    if k == 27:  # Esc key to breakloop and shutdown
        break

cv.destroyAllWindows()
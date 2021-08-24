import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)


    cv.imshow("Test", img)
    k = cv.waitKey(1)
    if k == 27:  # Esc key to breakloop and shutdown
        break

cv.destroyAllWindows()
import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

while(1):
    _, img = cam.read()
    cv2.imshow('original', img)

    crop_img = img[60:120, 0:160]

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    blur = cv2.bilateralFilter(gray, 5, 75, 75)

    _, thresh1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, k)

    cv2.imshow('opening', opening)

    contours1, _ = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(crop_img, contours1, -1, (0, 0, 255), 4)

    cv2.imshow('contour', crop_img)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
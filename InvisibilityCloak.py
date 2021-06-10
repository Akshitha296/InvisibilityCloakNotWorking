import cv2
import time
import numpy as np

#code to save output in avi format
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

#starting the webcam
cap = cv2.VideoCapture(0)

#allowing webcam to start by making the program sleep for 3 seconds (customizable)
time.sleep(3)
bg = 0

#capturing bg for 60 frames
for i in range(60):
    ret, bg = cap.read()

#flipping the bg
bg = np.flip(bg, axis = 1)

#reading captured frame until camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    #flipping image for consistency
    img = np.flip(img, axis = 1)
    #converting color from bgr to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #generating masks for red colour
    #numbers can be changed
    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask_1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_red, upper_red)
    mask_1 = mask_1+mask_2
    #open and expand the image where there is mask 1
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))
    #selecting only the part that doesn't have mask 1 and saving it to mask 2
    mask_2 = cv2.bitwise_not(mask_1)
    #keeping only images without the red
    res_1 = cv2.bitwise_and(img, img, mask = mask_2)
    #keeping images with red colour
    res_2 = cv2.bitwise_and(bg, bg, mask_1)
    #generating final output
    final_output = cv2.addWeighted(res_1, 1, res_2, 1, 0)
    output_file.write(final_output)
    #output
    cv2.iamshow("Invisible", final_output)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()
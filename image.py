import cv2
import numpy as np
import random

img = cv2.imread("./image_1.jpg", 0)
img_copy = img.copy()


def show_img(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)


def draw_contour(img):
    im_blur = cv2.GaussianBlur(img, (5, 5), 0)  # blur image
    im, thre = cv2.threshold(
        im_blur, 90, 255, cv2.THRESH_BINARY_INV)  # binary image
    kernel_dilate = np.ones((20, 20), np.uint8)  # dilate image kernel
    img_dilate = cv2.dilate(thre, kernel_dilate, iterations=1)  # dilate image
    kernel_erode = np.ones((14, 14), np.uint8)  # erode image kernel
    img_erode = cv2.erode(img_dilate, kernel_erode,
                          iterations=1)  # erode image
    contours, hierachy = cv2.findContours(
        img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # find contours
    contours_react = []  # contours reacts
    for i in range(len(contours)):
        (x, y, w, h) = cv2.boundingRect(contours[i])
        if(0.7 <= (w/h) <= 1.3) and (0.7 <= (h/w) <= 1.3):
            contours_react.append(contours[i])
    area_cnt = [cv2.contourArea(cnt) for cnt in contours_react]
    area_cnt_list = list(area_cnt)
    area_cnt_arr = np.array(area_cnt)
    contourArea_max = contours_react[area_cnt_list.index(area_cnt_arr.max())]
    (x, y, w, h) = cv2.boundingRect(contourArea_max)
    M = cv2.moments(contourArea_max)
    # O = (cx, cy) this is centor of contour
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    kytu = "x = " + str(cx) + ",  " + "y = " + str(cy)
    cv2.putText(img, kytu, (x, y),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1)
    return(img)


show_img(draw_contour(img))
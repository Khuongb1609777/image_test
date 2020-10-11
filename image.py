import cv2
import numpy as np
import os

img_url = "./INTELMARK.BMP"

img = cv2.imread(img_url, 0)
img_copy = img.copy()


def show_img(img):
    cv2.imshow(img_url, img)
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
    contourArea_max = contours_react[area_cnt_list.index(
        area_cnt_arr.max())]  # contour max area
    (x, y, w, h) = cv2.boundingRect(contourArea_max)
    print((x, y, w, h))
    M = cv2.moments(contourArea_max)
    # O = (cx, cy) this is centor of contour
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # draw bouding box
    # kytu = "x = " + str(cx) + ",  " + "y = " + str(cy)
    kytu = 'Centroid({}, {})'.format(cx, cy)
    cv2.putText(img, kytu, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)  # draw center O
    print
    return(img, cx, cy)


img_result, x, y = draw_contour(img_copy)
show_img(img_result)

# print(x,w,cx)

# 彩色均衡化提高对比度(降低明暗的影响)
import cv2 as cv
from module_displayImg import displayImg_a
import numpy as np
img = cv.imread(r"E:\images\All\2022-04-23T18_31_28+08_00\src.jpg")

img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# 对V通道进行直方均衡化
img_v = img_hsv[:, :, 2]
img_v = cv.equalizeHist(img_v)

img_hsv[:, :, 2] = img_v

img_histed = cv.cvtColor(img_hsv, cv.COLOR_HSV2BGR)


res = np.hstack((img, img_histed))
cv.imshow("res", res)
if cv.waitKey(0) == ord("q"):
  cv.destroyAllWindows()


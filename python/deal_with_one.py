from configparser import MAX_INTERPOLATION_DEPTH
from lib2to3.refactor import MultiprocessRefactoringTool
import cv2 as cv
import os
import numpy as np
from module_displayImg import displayImg_a

def matting(src: np.ndarray, mask: np.ndarray):
  """抠图，根据二值化的mask抠图

  Args:
      src (np.ndarray): 输入的图像，要求为三通道，并且在函数结束后会被修改
      mask (np.ndarray): 掩模，要求为单通道，且为二值化图像

  Returns:
      src: 抠图后的图像 
  """
  bgr_ls: list() = list(cv.split(src))
  for i in range(3):
    bgr_ls[i] = cv.bitwise_and(bgr_ls[i], mask)
  cv.merge(bgr_ls, src)
  return src


  
  

# path = "C:\\Users\\shiwenbo\\OneDrive\\images\\All\\2022-04-21T17_01_32+08_00\\src.jpg"
path = r"C:\Users\shiwenbo\OneDrive\images\All\2022-04-21T19_01_28+08_00\src.jpg"



lower_green = (29, 17, 46)
upper_green = (77, 255, 255)
src:np.ndarray = cv.imread(path)

src_2 = src.copy()
img = cv.cvtColor(src, cv.COLOR_BGR2HSV)
# inRange的输出green_mask为单通道二值图
green_mask: np.ndarray = np.zeros_like(img[:, :, 0])
cv.inRange(img, lower_green, upper_green, green_mask)
# 使用连通域分析也能实现去除杂点的降噪，而且是无损的
# 对green_mask做卷积核为(3,3)的开运算, 去除噪点, MORPH_RECT的效果明显比单纯(3,3)kernel好
cv.morphologyEx(green_mask, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), green_mask)

# 抠图
matting(src_2, green_mask)
displayImg_a(src_2)




img = src.copy()
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# OtSU大津法
otsu_threshold, img_bi_otsu = cv.threshold(img, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
# 对img_bi_otsu取反
img_bi_otsu = cv.bitwise_not(img_bi_otsu)


displayImg_a(img_bi_otsu)

matting(src_2, img_bi_otsu)
displayImg_a(src_2)
# src是根据img_bi_otsu去除了背景的图像
# src_2是bgr类型的图像副本，用于显示结果
# cv.imwrite("C:\\Users\\shiwenbo\\OneDrive\\images\\All\\2022-04-21T17_01_32+08_00\\cap.jpg", src)

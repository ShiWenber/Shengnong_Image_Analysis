import cv2 as cv
import os
import numpy as np
from module_displayImg import *

if __name__ == "__main__":
  path = r"C:\Users\shiwenbo\OneDrive\images\All\2022-04-21T17_01_32+08_00\src.jpg"
  lower_green = (29, 43, 46)
  upper_green = (77, 255, 255)
  img = cv.imread(path)
  cv.cvtColor(img, cv.COLOR_BGR2HSV, img)
  # inRange的输出green_mask为单通道二值图
  green_mask: np.ndarray = np.zeros_like(img[:, :, 0])
  cv.inRange(img, lower_green, upper_green, green_mask)
  # 使用连通域分析也能实现去除杂点的降噪，而且是无损的
  # 对green_mask做卷积核为(3,3)的开运算, 去除噪点, MORPH_RECT的效果明显比单纯(3,3)kernel好
  cv.morphologyEx(green_mask, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), green_mask)
  # 从path中获得文件路径
  displayImg_a(green_mask)

  nncomps, labels, stats, centroides = cv.connectedComponentsWithStats(green_mask)
  print("nncomps: ", nncomps)
  print("labels: ", labels)
  print("stats: ", stats)
  print("centroides: ", centroides)

  # 用随机数初始化色表
  colors = np.zeros((nncomps, 3), dtype=np.uint8)
  colors[0] = (0, 0, 0) # 背景色（第一行连通域的颜色）设置为黑色
  




  

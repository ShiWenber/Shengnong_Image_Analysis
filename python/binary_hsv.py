import time
import multiprocessing
import cv2 as cv
import numpy as np
from module_get_files_and_times_by_re import get_files_by_re
from multiprocessing import Pool
import os

def ProcessImg(path: str):
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
  dirpath, filename = os.path.split(path)
  cv.imwrite(dirpath + "\\" + "hsv_bin.jpg", green_mask)
  
def ProcessImg_cap(path: str):
  lower_green = (27, 18, 46)
  upper_green = (77, 255, 255)
  src:np.ndarray = cv.imread(path)
  img = src.copy()

  cv.cvtColor(img, cv.COLOR_BGR2HSV, img)
  # inRange的输出green_mask为单通道二值图
  green_mask: np.ndarray = np.zeros_like(img[:, :, 0])
  cv.inRange(img, lower_green, upper_green, green_mask)
  # 使用连通域分析也能实现去除杂点的降噪，而且是无损的
  # 对green_mask做卷积核为(3,3)的开运算, 去除噪点, MORPH_RECT的效果明显比单纯(3,3)kernel好
  cv.morphologyEx(green_mask, cv.MORPH_OPEN, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), green_mask)

  # 叠加掩模，将所有通道分别与掩模求与，得到掩模后的图像
  bgr_ls: list() = list(cv.split(src))
  for i in range(3):
    bgr_ls[i] = cv.bitwise_and(bgr_ls[i], green_mask)
  cv.merge(bgr_ls, src)

  dirpath, filename = os.path.split(path)
  cv.imwrite(dirpath + "\\" + "hsv_cap.jpg", src)

 

if __name__ == "__main__":
  # multiprocessing.freeze_support()
  start_time = time.time()
  paths = get_files_by_re(r"C:\Users\shiwenbo\OneDrive\images\All", "src.jpg")

  # 多进程处理，随着进程数量增加，多进程加速红利逐渐减小
  pool = Pool(6)
  for i in paths:
    pool.apply_async(ProcessImg_cap, args=(i,))
  pool.close()
  pool.join()
  print("time: ", time.time() - start_time)
  
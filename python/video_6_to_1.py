import os
import cv2
import numpy as np 
from time import time

dirpath_head = r"C:\Users\shiwenbo\OneDrive\images\gather\src"

start_time = time()

cl: list = []
for i in range(6):
  cl.append([])

for i in range(6):
  for filename in os.listdir(dirpath_head + f"{i}"):
    path = os.path.join(dirpath_head + f"{i}", filename)
    cl[i].append(path)

for i in range(6):
  cl[i].sort()

print("cl_time: ", time() - start_time)


def joint_img(img_path_6s):
  img_6s = list(map(cv2.imread, img_path_6s))
  res = np.vstack([np.hstack(img_6s[0:3]), np.hstack(img_6s[3:6])])
  return res 
# cl二维转置，未对齐的尾部会被丢弃，cl_inv 的元素为6个图片路径组成的列表
cl_inv = list(map(list, zip(*cl)))

# 创建视频写入对象
video = cv2.VideoWriter("6_to_1.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10, (640*3, 480*2))

# 合成6个图片为1个图片，并遍历之
for i in map(joint_img, cl_inv):
  video.write(i)
video.release()
print("time :", time() - start_time)

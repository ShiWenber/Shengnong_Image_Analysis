def take_part_by_reservations(input: list, index: int, reservations_num: int = 6, delt_minute: int = 30):
  """按照机位给数据分类，最后返回一个二维列表，每个元素就是同一机位数据组成的列表

  Args:
      input (list): 已经按时间先后顺序排好序的二维数据列表，其中一列应该是 date_time 列表，date_time 的格式为 "%Y-%m-%dT%H_%M_%S"
      index (int): date_time 列表在 input 中的索引
      reservations_num (int, optional): 机位数量. Defaults to 6.
      delt_minute (int, optional): 一轮遍历一次所有机位，每轮遍历任务开始的间隔时间. Defaults to 30.

  Returns:
      list: 返回 cl，cl[0] 表示第一机位数据列表， cl[1] 表示第二机位数据列表，依次类推, cl[i] 的格式与 input 相同
  """
  import datetime

  temp = datetime.datetime.strptime(input[0][index], "%Y-%m-%dT%H_%M_%S")
  cl = []
  for i in range(reservations_num):
    cl.append([])
  j: int = 0
  for i in input:
    # hours = 0.8 * delt_minute / 60, 0.8的系数是为了容忍误差, 如果相邻的两个数据时间差小于0.8 * delt_minute / 60, 则认为是同一轮的不同机位的数据
    if datetime.datetime.strptime(i[index], "%Y-%m-%dT%H_%M_%S") - temp <= datetime.timedelta(hours=0.8 * (delt_minute / 60)):
      # 同次不同机位
      temp = datetime.datetime.strptime(i[index], "%Y-%m-%dT%H_%M_%S")
      cl[j].append(i)
    else:
      # 不同次
      temp = datetime.datetime.strptime(i[index], "%Y-%m-%dT%H_%M_%S")
      j = 0
      cl[j].append(i)
    j += 1
    j = j % reservations_num
  return cl


import os
import re
import pandas as pd
from module_get_files_and_times_by_re import get_files_and_times_by_re
from module_gather_files import gather_files
from time import time
start_time = time()


# 读取csv文件
# files_and_times = get_files_and_times_by_re(r"C:\Users\shiwenbo\OneDrive\images\All", r'src.jpg')
files_and_times = get_files_and_times_by_re(r"E:\images\All", r'proc.jpg')

print(files_and_times)

# 按照机位分类
cl = take_part_by_reservations(files_and_times, 1, 6, 30)

# 按照分类复制聚集文件
idx: int = 0
for i in cl:
  # gather_files(i, r"C:\Users\shiwenbo\OneDrive\images\gather\src" + str(idx))
  gather_files(i, r"E:\dataset\shengnong\label" + str(idx))

  idx += 1
print("time: ", time() - start_time)
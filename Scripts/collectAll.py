# 将所有文件合并
from gc import collect
import os
from traceback import print_tb
from typing import Set

collected_files = []

def get_files(base, all_files=set()):

  os.chdir(base)
  # print(base)

  # for file in os.listdir():
  #   #   os.rename(file, file.replace("\uf03a", "_"))
  #     print(os.popen(f"mv {file} .\\All\\" ).read())
  #     collected_files.append(base + "\\" + file)
  
#   递归遍历文件
  for file in os.listdir():
    if (not os.path.isdir(base + "\\" + file)) and (file.endswith(".jpg") or file.endswith(".csv")):
      all_files.add(base)
    elif not os.path.isdir(base + "\\" + file):
      continue
    else:
      get_files((base + "\\" + file), all_files)
  return all_files

# for i in os.listdir(os.getcwd()):
    # print(i)

all_files = get_files(os.getcwd())
for i in all_files:
  print(os.popen(f"mv {i} .\\All\\" ).read())
  print(i)

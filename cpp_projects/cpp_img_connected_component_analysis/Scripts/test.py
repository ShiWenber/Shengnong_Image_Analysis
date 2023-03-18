import os
import re

# print(os.getcwd())
# print("input base path, or using the default base path (F:\dataFileForAll\OneDrive\images):")
# input_base = input()
# if input_base == "":
#   input_base = r"F:\dataFileForAll\OneDrive\images"

# os.chdir(input_base)
# print(os.getcwd())

os.getcwd()
print('--------------------------------------')
print("renamed files")
print("--------------------------------------")

for i in os.listdir(os.getcwd()):
  if r'.' not in i and re.match(r'\d-\d+', i) != None:
    ls = list(map(int, i.split('-')))
    # 重命名文件
    os.rename(i, f'2022-{ls[0]:0>2d}-{ls[1]:0>2d}')
    print(f'{i} -> 2022-{ls[0]:0>2d}-{ls[1]:0>2d}')
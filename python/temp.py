from module_get_files_and_times_by_re import get_files_and_times_by_re
import os
from shutil import copyfile


if __name__ == "__main__":
    files_and_times = get_files_and_times_by_re(r"E:\images\All", r'src.jpg')
    index_strs = []
    for root, dirs, files in os.walk(r"E:\dataset\shengnong\label"):
        for file in files:
            path = os.path.join(root, file)
            index_str = file.split(".")[0]
            index_strs.append(index_str)
    
    print(index_strs)
    print(len(index_strs))
    
    files_and_times.sort(key=lambda x: x[0])
    print(files_and_times)
    print(len(files_and_times))
    
    
    i = 0
    j = 0
    res = []
    while i < len(index_strs) and j < len(files_and_times):
        if index_strs[i] == files_and_times[j][1]:
            res.append(files_and_times[j][0])
            print("i = {}, j = {}".format(i, j))
            print("index_strs[i] = {}, files_and_times[j][1] = {}".format(
                index_strs[i], files_and_times[j][1]))
            i += 1
            j += 1
        else:
            j += 1
    
    
    # 复制文件
    for i in range(len(res)):
        copyfile(res[i], r"E:\dataset\shengnong\image\{}.jpg".format(index_strs[i]))
    # print(files_and_times)

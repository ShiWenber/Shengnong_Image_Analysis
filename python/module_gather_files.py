

def gather_files(files: list, dst: str):
  """聚集文件到指定目录

  Args:
      files (list(str)): [文件绝对路径,拍摄日期]的二元组列表
      dst (str): 目的路径
  """
  from shutil import copyfile
  import os
  # files
  for path, date_time in files:
    # 复制文件, 从路径中获取文件名的方法：os.path.basename(i), i.split("\\")[-1]
    name, ext = os.path.basename(path).split(".")
    copyfile(path, os.path.join(dst, date_time + "." + ext))
  


if __name__ == "__main__":
  # copyfile使用多进程加速失效，没有任何文件被复制
  from module_get_files_and_times_by_re import get_files_and_times_by_re
  import os
  from time import time
  start_time = time()
  gather_files(get_files_and_times_by_re(os.getcwd() + r"\All", "hsv_cap.jpg"), os.getcwd() + r"\gather\hsv_cap")
  print("time:", time() - start_time)



  # # 多进程提高速度，多进程加速脚本
  # from get_files_and_times_by_re import get_files_and_times_by_re
  # from multiprocessing import Pool
  # from shutil import copyfile
  # from time import time
  # import os
  # start_time = time()
  # pool = Pool(4)
  # path_datetimes = get_files_and_times_by_re(os.getcwd() + r"\All", "hsv_cap.jpg")
  # for path, datetime in path_datetimes:
  #   pool.apply_async(copyfile, args=(path, datetime, os.getcwd() + r"\gather\hsv_cap",))
  # pool.close()
  # pool.join()

  # print("time: ", time() - start_time)
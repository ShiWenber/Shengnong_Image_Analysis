from turtle import title
import cv2 as cv
import numpy as np


def DisplayImg(img: np.ndarray, title: str = "Image", wait: int = 0):
    """展示图片

    Args:
        img (np.ndarray): 图片
        title (str, optional): 标签. Defaults to "Image".
        wait (int, optional): 等待时间，单位为毫秒. Defaults to 0.
    """
    cv.imshow(title, img)
    k = cv.waitKey(wait)
    if k == ord("q"):
      cv.destroyAllWindows()
    elif k == ord("s"):
      cv.imwrite("src.png", img)
def DisplayImg(img_ls: list, title_ls: list, wait:int=0):
  """展示图片
  
  Args:
      img_ls (list): 图片列表
      title_ls (list): 标签列表
      wait (int, optional): 等待时间，单位为毫秒. Defaults to 0.
  """
  for i in range(len(img_ls)):
    cv.imshow(title_ls[i], img_ls[i])
  k = cv.waitKey(wait)
  if k == ord("q"):
    cv.destroyAllWindows()
  elif k == ord("s"):
    for i in img_ls:
      cv.imwrite(title_ls[i]+"jpg", img_ls[i])


# main


if __name__ == "__main__":
  src = cv.imread(r"C:\Users\shiwenbo\OneDrive\images\All\2022-04-21T17_01_32+08_00\src.jpg")

  print(type(src))

  hsv = np.zeros_like(src)


  cv.cvtColor(src, cv.COLOR_BGR2HSV, hsv)
  hsv_h = hsv[:, :, 0]
  hsv_s = hsv[:, :, 1]
  hsv_v = hsv[:, :, 2]
  #  同时显示三通道的灰度图(每张都只有单通道)
  # DisplayImg([hsv_h, hsv_s, hsv_v], ["h", "s", "v"], 0)


  # hsv中绿色的范围35-77,43-255,46-255
  # 对三个通道分别进行选定参数二值化
  cv.namedWindow("h")
  cv.namedWindow("s")
  cv.namedWindow("v")

  cv.createTrackbar("h_c", "h", 0, 255, lambda x: None)
  cv.createTrackbar("s_c", "s", 0, 255, lambda x: None)
  cv.createTrackbar("v_c", "v", 0, 255, lambda x: None)

  binary_h = np.zeros_like(hsv_h)
  binary_s = np.zeros_like(hsv_s)
  binary_v = np.zeros_like(hsv_v)

  while True:
    
    
    img_ls = [binary_h, binary_s, binary_v]
    title_ls = ["h", "s", "v"]
    for i in range(len(img_ls)):
      cv.imshow(title_ls[i], img_ls[i])
    k = cv.waitKey(1)
    if k == ord("q"):
      cv.destroyAllWindows()
      break
    elif k == ord("s"):
      for i in img_ls:
        cv.imwrite(title_ls[i]+"jpg", img_ls[i])

    h_c = cv.getTrackbarPos("h_c", "h")
    s_c = cv.getTrackbarPos("s_c", "s")
    v_c = cv.getTrackbarPos("v_c", "v")

      
    cv.adaptiveThreshold(hsv_h, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, h_c, binary_h)
    cv.adaptiveThreshold(hsv_s, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, s_c, binary_s)
    cv.adaptiveThreshold(hsv_v, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, v_c, binary_v)

    






  

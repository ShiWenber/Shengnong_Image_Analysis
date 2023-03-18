import cv2 as cv
import numpy as np
def displayImg_a(img: np.ndarray, title: str = "Image", wait: int = 0):
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
def displayImg(img_ls: list, title_ls: list, wait:int=0):
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


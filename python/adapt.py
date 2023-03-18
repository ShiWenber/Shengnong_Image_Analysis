from email.mime import image
from module_displayImg import displayImg
import cv2 as cv
import sys

if __name__ == "__main__":
  img = cv.imread(r"C:\Users\shiwenbo\OneDrive\images\All\2022-04-21T17_01_32+08_00\src.jpg")  
  if img is None:
    print("Error: Could not load image")  
    sys.exit()

  img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  cv.imshow("img_gray", img_gray)
  print(img_gray.shape)


  # OTSU大津法
  otsu_threshold, img_bi_otsu = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
  cv.imshow("img_bi_otsu1", img_bi_otsu)
  otsu_threshold, img_bi_otsu = cv.threshold(img_gray, 0, 255, cv.THRESH_OTSU)
  cv.imshow("img_bi_otsu2", img_bi_otsu)

  k = cv.waitKey(0)
  if k == ord("q"):
    cv.destroyAllWindows()

  # 三角法确定阈值
  # tri_threshold, img_bi_tri = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
  # tri_threshold, img_bi_tri = cv.threshold(img_gray, 0, 255, cv.THRESH_TRIANGLE)

  # 滑动条
  # cv.namedWindow("OTSU")
  # while True:
    

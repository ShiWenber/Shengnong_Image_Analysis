import cv2 as cv
import base64
import numpy as np
import json
import pycocotools.mask as mask_util


    

def mask_str2img(path: str) -> np.ndarray:
  # json中可能有中文utf-8防止乱码
  file = open(path, "r", encoding="utf-8")
  content = file.read()
  file.close()

  results = json.loads(content)
  res = {}
  for i in results['labels']:
    name = i["name"]
    x1 = i["x1"]
    y1 = i["y1"]
    x2 = i["x2"]
    y2 = i["y2"]
    mask_str = i["mask"]
    shape = i["shape"]
    meta = i["meta"]
    meta__actions = meta["actions"]
    size = i["size"]
    size__height = size["height"]
    size__width = size["width"]
  
    
    rle_obj = {"counts": mask_str,
               "size": [size__height, size__width]}
    # easydl 数据标注 json 文件中 mask 属性的值为图片，采用的编码方式为 RLE
    mask = mask_util.decode(rle_obj)
    # decode 方法返回的是一个二值化的 np.ndarray 单通道类型的图片像素值取值为 0 或者 1, 乘以 255 以便于后续的 cv2.imshow 显示
    mask *= 255
    res[name] = mask
  return res
  

if __name__ == "__main__":
  path = "./2022-04-22T06_00_22.json"   
  dic = mask_str2img(path)
  for i in dic:
    cv.imshow(i, dic[i])
    if cv.waitKey(0) == ord("q"):
      cv.destroyAllWindows()



  

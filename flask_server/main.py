import glob
import numpy as np
import torch
import os
import cv2
from torch.utils.tensorboard import SummaryWriter
# from model.unet_model import UNet
# from model.unet_model_seattention import UNet
from model.unet_model_mobilevit import UNet
import time

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid
from PIL import Image
import os
import time
import base64
import json
from flasgger import Swagger, swag_from
from io import BytesIO
from oss_utils import OssUtils

# 全局网络设置

## 选择设备
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
## 加载网络,图片单通道1，分类为1。
net = UNet(n_channels=1, n_classes=1)
## 载入到device中
net.to(device=device)
## 加载参数
net.load_state_dict(torch.load('./best_model2023-01-20T01_50_43shengnong_unetmvit_60_4.pth', map_location=device))
## 测试
net.eval()

def segmentation(img: np.ndarray, path: str = None, uuid_str: str = None):
    """图像分割

    Args:
        img (np.ndarray): 输入图像
        path (str, optional): 从本地路径图片. Defaults to None.
        uuid_str (str, optional): 处理任务uuid编号. Defaults to None.

    Returns:
        _type_: _description_
    """
    # 生成uuid标识任务
    if uuid_str == None:
        uuid_str = uuid.uuid4().hex
    # 如果path 不为none，使用path
    if path != None:
        print("path:", path)
        # 读取
        img = cv2.imread(path)
    start_time = time.time()
    # # 选择设备
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # # 加载网络,图片单通道1，分类为1。
    # net = UNet(n_channels=1, n_classes=1)
    # # 载入到device中
    # net.to(device=device)
    # # 加载参数
    # net.load_state_dict(torch.load('./best_model2023-01-20T01_50_43shengnong_unetmvit_60_4.pth', map_location=device))
    # # 测试
    # net.eval()

    # tensorboard
    # writer = SummaryWriter(log_dir='logs', comment='UNet')

    # 读取图片路径
    # tests_path = glob.glob("shengnong/valid/*")

    # 转灰度
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 转为batch为1,通道为1的数组
    img = img.reshape(1,1,img.shape[0], img.shape[1])
    # img = img.reshape(1,img.shape[0], img.shape[1])
    # 转tensor
    img_tensor = torch.from_numpy(img)
    # 转到device中
    img_tensor = img_tensor.to(device=device, dtype=torch.float32)
    # 预测
    pred = net(img_tensor)
    # 提取结果
    pred = np.array(pred.data.cpu()[0])[0]
    # 处理结果
    pred[pred >= 0.5] = 255
    pred[pred < 0.5] = 0

    print(f"{uuid_str} time:", time.time() - start_time)
    return pred 



app = Flask(__name__)
Swagger(app)
# app.config['JSON_AS_ASCII'] = False # 解决中文乱码问题

@app.route("/test",methods = ["GET"])
def test():
    # 用于测试服务是否并行
    time.sleep(1)
    return "0"


@app.route("/",methods=["GET"])
def show():
    return "leaf area segmentation api"

@app.route("/getImgRes",methods = ["POST"])
@swag_from("get_img_res.yml")
def get_img():
    file = request.files['file']
    base_path = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(base_path, "temp")):
        os.makedirs(os.path.join(base_path, "temp"))
    file_name = uuid.uuid4().hex
    upload_path = os.path.join(base_path, "temp", file_name)
    file.save(upload_path)
    res_img = segmentation(None, upload_path, file_name)
    # # 图片转base64
    # base64_data = base64.b64encode(res_img)
    # # 构建返回数据
    # res = {"img": base64_data.decode()}
    # 返回图片
    ## 全部在内存缓冲区完成能提高性能（如果使用imwrite再保存会导致从外部磁盘读取的io操作）
    _, img_encoded = cv2.imencode('.jpg', res_img)
    img_binary = img_encoded.tobytes()
    image_binary_stream = BytesIO(img_binary)
    return send_file(
        image_binary_stream,
        mimetype='image/jpeg',
        as_attachment=True,
        download_name='result.jpg'
    )

@app.route("/getBase64Res",methods = ["POST"])
@swag_from("get_base64_res.yml")
def image():
    data = request.get_json()
    image_data = data['image_data']

    # 将base64字符串转换为二进制数据
    image_binary_data = base64.b64decode(image_data)

    # 转换二进制数据为numpy数组
    image_array = np.frombuffer(image_binary_data, np.uint8)

    # 转化为opencv图像的ndarray格式
    image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)

    # 断言检查image的类型是否为ndarray
    assert type(image) is np.ndarray

    # 图像处理部分
    res_img = segmentation(image)

    # 将内存中的图像转换为base64字符串
    result, image_data = cv2.imencode('.jpg', res_img)
    image_data = base64.b64encode(image_data).decode('utf-8')
    return jsonify({'image_data': image_data})


@app.route("/getRes",methods = ["POST"])
@swag_from("get_res.yml")
def leaf_area_index():
    # 百分比0-100
    leaf_area_index = 0
    data = request.get_json()
    url = data['url']
    image = OssUtils.read_img_by_url(url)

    # 断言检查image的类型是否为ndarray
    assert type(image) is np.ndarray

    # 图像处理部分
    res_img = segmentation(image)

    # 统计像素
    leaf_area_index = np.sum(res_img == 255) / (res_img.shape[0] * res_img.shape[1]) * 100

    # 将内存中的图像上传到oss TODO

    return jsonify({'leaf_area_index': leaf_area_index})


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5005,debug=True)

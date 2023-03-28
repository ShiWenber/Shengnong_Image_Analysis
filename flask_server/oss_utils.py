# -*- coding: utf-8 -*-
'''
!! 特别注意：object_stream.read()只能执行读取一次，当前面读取之后，后面的读取都为空
'''
import oss2
import shutil
from io import BytesIO
import cv2
import numpy as np
from PIL import Image

class OssUtils:
    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
    __auth = oss2.Auth('AccessKeyId', 'AccessKeySecret') # 填写AccessKeyId和AccessKeySecret
    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称。

    __endpoint = 'https://oss-cn-hangzhou.aliyuncs.com'

    __bucket_name = 'plants-images'

    __bucket = oss2.Bucket(__auth, __endpoint, __bucket_name)
    # bucket.get_object的返回值是一个类文件对象（File-Like Object），同时也是一个可迭代对象（Iterable）。
    # 填写Object的完整路径。Object完整路径中不能包含Bucket名称。

    __url_prefix = '' # 这里应该是个人设置的oss域名

    @classmethod
    def get_auth(cls):
        return cls.__auth
    
    @classmethod
    def get_bucket(cls):
        return cls.__bucket

    @classmethod
    def get_endpoint(cls):
        return cls.__endpoint
    
    @classmethod
    def get_bucket_name(cls):
        return cls.__bucket_name
    
    @classmethod
    def get_url_prefix(cls):
        return cls.__url_prefix

    @classmethod
    def set_bucket(cls, endpoint: str, bucket_name: str):
        """设置bucket

        Args:
            endpoint (str): 示例: https://oss-cn-hangzhou.aliyuncs.com
            bucket_name (str): 示例: plants-images
        """
        cls.__bucket = oss2.Bucket(cls.__auth, endpoint, bucket_name)
    
    @classmethod
    def set_auth(cls, access_key_id: str, access_key_secret: str):
        """设置auth

        Args:
            access_key_id (str): 示例: lsidjfisoajsfoasif
            access_key_secret (str): 示例: sjdfoasidjiofaj
        """
        cls.__auth = oss2.Auth(access_key_id, access_key_secret)

    @classmethod
    def set_endpoint(cls, endpoint: str):
        """设置endpoint

        Args:
            endpoint (str): 示例: https://oss-cn-hangzhou.aliyuncs.com
        """
        cls.__endpoint = endpoint
    
    @classmethod
    def set_bucket_name(cls, bucket_name: str):
        """设置bucket_name

        Args:
            bucket_name (str): 示例: plants-images
        """
        cls.__bucket_name = bucket_name
    
    @classmethod
    def set_url_prefix(cls, url_prefix: str):
        """设置url_prefix

        Args:
            url_prefix (str): 示例: http://oss.boer.ink
        """
        cls.__url_prefix = url_prefix


    @staticmethod
    def is_image(object_stream: oss2.models.GetObjectResult):
        """判断文件类型是否为图片，并返回图片应该保存的后缀格式和对应编码名称，目前识别:
        image/jpeg, image/png, image/gif, image/bmp

        Returns:
            res: bool, 是否为图片
            file_ext: str, 图片后缀
            coding_type: str, 图片编码
        """
        
        res = False
        file_ext = ''
        coding_type = ''
        # 判断文件类型是否为图片
        if (object_stream.content_type == 'image/jpeg'):
            return True, 'jpg', 'jpeg'
        elif (object_stream.content_type == 'image/png'):
            return True, 'png', 'png'
        elif (object_stream.content_type == 'image/gif'):
            return True, 'gif', 'gif'
        elif (object_stream.content_type == 'image/bmp'):
            return True, 'bmp', 'bmp'


    @staticmethod
    def read_img(object_path: str):
        object_stream = OssUtils.__bucket.get_object(object_path)
        is_img, file_ex, file_type= OssUtils.is_image(object_stream)
        if (is_img):
            image = cv2.imdecode(np.frombuffer(object_stream.read(), np.uint8), cv2.IMREAD_COLOR)
            # 由于get_object接口返回的是一个stream流，需要执行read()后才能计算出返回Object数据的CRC checksum，因此需要在调用该接口后进行CRC校验。
            if object_stream.client_crc != object_stream.server_crc:
                print("The CRC checksum between client and server is inconsistent!")
                raise Exception("The CRC checksum between client and server is consistent!") 
            return image 
    
    @staticmethod
    def read_img_by_url(url: str):
        """通过url读取图片

        Args:
            url (str): 图片url

        Returns:
            np.ndarray: 图片
        """
        # 从 url 中提取 object_path，示例: https://plants-images.oss-cn-hangzhou.aliyuncs.com/images/1.jpg?Expires=1610000000&OSSAccessKeyId=LTAI5t9pSPR9CJrX2VEjG9ty&Signature=xxxxx
        # 从中取出 object_path: images/1.jpg
        ##  repr(a)[1:-1] 将 str 变量 a 转换为raw字符串
        object_path = repr(url)[1:-1]
        print(object_path)
        img = OssUtils.read_img(object_path)
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        return img

    @staticmethod
    def upload_img(img: np.ndarray, object_path: str):
        """上传图片

        Args:
            img (np.ndarray): 图片
            object_path (str): 上传到oss的路径
        """
        # 将图片转换为jpg格式
        img = cv2.imencode('.jpg', img)[1]
        # 将图片转换为bytes
        img_bytes = BytesIO(img)
        # 上传到oss
        OssUtils.__bucket.put_object(object_path, img_bytes)



if __name__ == "__main__":
    # 读取图片
    # img = OssUtils.read_img('images/01.png')
    img = OssUtils.read_img_by_url(r"http://oss.boer.ink/images/01.png")
    cv2.imwrite('test.png', img)

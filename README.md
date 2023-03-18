# Shengnong_Image_Analysis

非常抱歉，此模块中的数据集均采用绝对路径，因此无法直接运行，需要自行修改路径

Cpp部分实现了cpp—opencv的连通域分析和连通域合并，最终将这些连通域合并为2个最大的部分（在整体项目中弃用）

Python部分实现了图像数据的按拍摄时间分机位，各机位合成视频，python-opencv基于颜色的图像分割

flask_server部分实现了深度学习图像分割模型的服务化，主要用来从图像中分割出植物叶片，目前仅有叶片，背景二分类的模型

## Directory Structure

```bash
Shengnong_Image_Analysis
├── cpp_projects (visual studio c++ projects)
├── python (python code)
├── flask_server (flask server，深度学习图像分割模型的服务化)
└── README.mdn
```
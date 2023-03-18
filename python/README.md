# CV

非常抱歉，此模块中的数据集均采用绝对路径，因此无法直接运行，需要自行修改路径

## opencv

[自适应阈值二值化算法 - bldong - 博客园 (cnblogs.com)](https://www.cnblogs.com/polly333/p/7269153.html)

[(148条消息) 与二值化阈值处理相关的OpenCV函数、方法汇总,便于对比和拿来使用_昊虹图像算法的博客-CSDN博客](https://blog.csdn.net/wenhao_ir/article/details/125592598)
目前只尝试了OTSU大津法，效果相当好，但是只能根据灰度图的深浅，要提取特定颜色做不到
todo: 尝试先基于颜色提取较宽泛的色域，然后在进行OTSU大津法等自适应阈值方法
而adaptiveThreshold则更多的提取边缘，色彩相近的区域块则一般呈现雪花状

## plantcv

[(148条消息) PlantCV 农业自动化中的机器视觉库_imagegeek的博客-CSDN博客](https://blog.csdn.net/xss20072754/article/details/112696916?ops_request_misc=%7B%22request%5Fid%22%3A%22166226579016782248597962%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=166226579016782248597962&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-112696916-null-null.142^v46^pc_rank_34_1&utm_term=plantcv&spm=1018.2226.3001.4187)

[Deep learning, hydroponics, and medical marijuana - PyImageSearch](https://pyimagesearch.com/2018/10/15/deep-learning-hydroponics-and-medical-marijuana/)

## 图像语义分割

[全文阅读--XML全文阅读--中国知网 (cnki.net)](https://kns.cnki.net/KXReader/Detail?invoice=IdEhv2qgKqmGBT3k%2Be3o1CNlS0hNkf0eBtKJf1nMeWyf3OL1k4c0avyRgqQmQiMwj5ly0i3rl3qpz5loO3%2BLDxpnrMPiVoC%2Fvh4qXCUBr0sRHNyc2pGEFHdpNtIgwR8NZqQo6O2a7hCW0%2Bn9jixXxuoUiLiueeMLjiHKcneB0aM%3D&DBCODE=CJFD&FileName=BJLY201811015&TABLEName=cjfdlast2018&nonce=8D07C9727C6A4144B70C6B6528EA53BB&uid=&TIMESTAMP=1662362410029)

基于全卷积网络的植物叶片分割算法


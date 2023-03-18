# flask_server

## 模块简介

该模块使用的是flask框架，服务器使用的是gunicorn，swagger文档使用flasgger库生成，gunicorn的设置文件为gunicorn.conf.py

## 配置说明

main.py代码中调用的模型参数文件，使用如下连接下载：

https://pan.baidu.com/s/1PhgV4STqc1Ie7vjJf7eCig?pwd=h3i1

该模型应放在main.py同目录下

## 使用说明

启动后端的命令为：

```bash
gunicorn -c gunicorn.conf.py main:app    
```

该命令写在了run.sh中，可以直接运行run.sh启动后端

swagger文档使用的是flasgger库构建的，运行起来后端后使用 <url-root>/apidocs 打开swagger文档

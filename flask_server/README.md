# flask_server

main.py代码中使用的模型下载位置，该模型应放在main.py同目录下

该模块使用的是flask框架，服务器使用的是gunicorn，使用gunicorn启动main.py，设置文件为gunicorn.conf.py，启动后端的命令为：

```bash
gunicorn -c gunicorn.conf.py main:app    
```

该命令写在了run.sh中，可以直接运行run.sh启动后端

代码中调用的模型参数文件，使用如下连接下载：

https://pan.baidu.com/s/1PhgV4STqc1Ie7vjJf7eCig?pwd=h3i1
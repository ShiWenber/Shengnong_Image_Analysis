# `hello_opencv`

这一部分实现了cpp—opencv的连通域分析和连通域合并，最终将这些连通域合并为2个最大的部分（因为我们需要将图像中的两株植物区分开）。

This part implements the connected component analysis and merging of cpp-opencv, and finally merges these connected components into two largest parts (because we need to distinguish the two plants in the image).

## 脚本使用

项目目录下的`*.py`脚本使用方式：

1. 必须放置在需要处理的压缩包的同级目录下执行，例如：
如果压缩包放在`D:\Pros`目录下，则需要使用

```powershell
PS D:\Pros> python tarAll.py
```

其他几个脚本同样
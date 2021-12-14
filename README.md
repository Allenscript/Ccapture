

# <img src="https://icons.iconarchive.com/icons/dakirby309/windows-8-metro/128/Apps-Screenshot-Metro-icon.png" height="28px"/>       Ccapture ⭐

> 这是一个小工具，在进行直播学习或者在线视频的时候，能够自动的对PPT区域进行截图,自动比对当前画面区域PPT是否更新，及时截屏

#
<!-- ## 界面 -->
### 界面
<img src="https://github.com/Allenscript/Ccapture/blob/master/images/screenshot.png">

## 运行准备

- pip install -r reqrement.txt



## 运行
```
python ./main.py
```

## 打包

>如果需要打包成exe程序，请按以下步骤
```
pip install pyinstaller
pyinstaller  -Fw main.spec

```

## 个性化
> 如果需要定制程序图标或界面内按钮图标
<br> - 替换screenshot.ico
<br> - 使用wxPython自带的img2py.py 脚本将图片转换为python文件

```
#图片
python .\img2py.py -n <var> .\picture.png images2.py
#图标
python .\img2py.py -n AppIcon .\screenshot.ico images.py

```

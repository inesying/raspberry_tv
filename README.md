# raspberry_tv

## 树莓派环境配置


## shift.py

![image](https://github.com/inesying/raspberry_tv/blob/main/rasp_tv.gif)

实现三种功能的切换

功能一：显示李子柒b站粉丝数和粉丝数变化

功能二：显示当地实时天气

功能三：循环显示gif和图片

功能一question：

1.获取粉丝数的办法

修改https://api.bilibili.com/x/relation/stat?vmid=xxxxx  中的vmid实现获取不同up主的粉丝情况

获取vmid的办法

![image](https://github.com/inesying/raspberry_tv/blob/main/checkapi.png)

功能二：获取天气

 https://dev.qweather.com/申请相应的key
 
 功能三： gif的循环播放
 
 
 
 其他问题：
 
 1.中文的显示：'simfang.ttf'仿宋体
 
 2.监听按键，按键变化实现三种功能的切换
 
 3.icon下载：天气icon from：和风天气，bilibili icon from：阿里icon
 
 

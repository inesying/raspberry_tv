

# -*- coding: utf-8 -*-
import spidev as SPI
import RPi.GPIO as GPIO


import ST7789
import time
import requests
import json
import os
from PIL import Image,ImageDraw,ImageFont,ImageColor
import numpy as np
from gif import AnimatedGif
import threading
port = 1

#key init
#GPIO define
RST_PIN        = 25
CS_PIN         = 8
DC_PIN         = 24

KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_icon_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

RST = 27
DC = 25
BL = 24
bus = 0 
device = 0 


# 240x240 display with hardware SPI:
disp = ST7789.ST7789(SPI.SpiDev(bus, device),RST, DC, BL)
disp.Init()

# Clear display.
disp.clear()

#init GPIO
# for P4:
# sudo vi /boot/config.txt
# gpio=6,19,5,26,13,21,20,16=pu
GPIO.setmode(GPIO.BCM) 
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_icon_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

fans = 0
fansChange = ''
nowtemp=''
icon='101'
event=0
#chinese character and set size
newfont=ImageFont.truetype('simfang.ttf',30)
smallfont=ImageFont.truetype('simfang.ttf',15)

def updateBFans():
    global fans
    global fansChange
    print('check bb')
    try:
        # 获取李子柒的粉丝数，修改vmid获取不同up主粉丝数
        r = requests.get('https://api.bilibili.com/x/relation/stat?vmid=19577966')
        fans = r.json()['data']['follower']
        file = "blog.log"
        # 记录6小时内粉变动
        if os.path.exists(file):
            print('logs')
            with open(file, "r") as f:
                data = json.load(f)
            arr = []
            for obj in data:
                if obj['t']+3600*6 > int(time.time()):
                    arr.append(obj)
            arr.append({'t':int(time.time()),'f':fans})
            with open(file, "w+") as f:
                f.write(json.dumps(arr))
        else:
            with open(file, "w+") as f:
                f.write(json.dumps([{'t':int(time.time()),'f':fans}]))
        with open(file, "r") as f:
            data = json.load(f)
        countFans = data[len(data)-1]['f'] - data[0]['f']
        fansChange = '+%d'%countFans if countFans >=0 else '%d'%countFans
    except Exception as e:
        print(e)

def updateWeather():
    global client
    global nowtemp
    global icon

    # 获取天气
    try:
        ##https://dev.qweather.com/ 申请key
        r = requests.get(
            'https://devapi.qweather.com/v7/weather/now?location=101280601&key=3845091bb8c646219620211eaed8d873')##location城市代码key网站申请
        nowtemp = r.json()['now']['temp']
        icon=r.json()['now']['icon']
    except Exception as e:
        print(e)

def Showgif():
    print('showgif')
    try:
       gif_player = AnimatedGif(disp.ShowImage,Xstart=0,Ystart=0,width=240, height=240, folder=".")
    except Exception as e:
        print(e)

def loop():#loop renew
    time.sleep(5)
    while True:
        updateBFans()
        updateWeather()
        if time.localtime().tm_min == 2:
            updateWeather()
        else:
            f = open('weatherData.log')
            txt = f.read()
            f.close()
        time.sleep(60)

def getmotion():#key change
    global event

    # with canvas(device) as draw:
    if GPIO.input(KEY_UP_PIN): # button is released
        pass       
    else: # button is iconed:
        print("Up")
        time.sleep(0.5)
        event=(event+1)%2#切换成下一个事件
        
    if GPIO.input(KEY_LEFT_PIN): # button is released
        pass           
    else: # button is iconed:
        print("left")
        time.sleep(0.5)
        event=(event+2)%2#切换成上一个事件
        
    if GPIO.input(KEY_RIGHT_PIN): # button is released
        pass      
    else: # button is iconed:
        print("right")
        time.sleep(0.5)
        event=(event+1)%2#切换成下一个事件
        
    if GPIO.input(KEY_DOWN_PIN): # button is released
        pass      
    else: # button is iconed:
        print("down")
        time.sleep(0.5)
        event=(event+2)%2#切换成上一个事件
        
    if GPIO.input(KEY_icon_PIN): # button is released
        pass         
    else: # button is iconed:
        print("none")
        time.sleep(0.5)
        
    if GPIO.input(KEY1_PIN): # button is released
        pass        
    else: # button is iconed:
        print("event1")
        time.sleep(0.5)
        event=0#切换成事件1
        
    if GPIO.input(KEY2_PIN): # button is released
        pass        
    else: # button is iconed:
        print("event2")
        time.sleep(0.5)
        event=1
        
    if GPIO.input(KEY3_PIN): # button is released
        pass       
    else: # button is iconed:
        print("event3")
        time.sleep(0.5)
        event=2

def apds():#monitor whether the key change
    try:
        while True:
            time.sleep(0.5)
            while True:
                motion = getmotion()
    finally:
        GPIO.cleanup()
        print("Bye")

if __name__ == '__main__':
    dataLoop = threading.Thread(target=loop)
    dataLoop.start()

    apdsLoop = threading.Thread(target=apds)
    apdsLoop.start()
    checkTimes=0
    

    while True:
        if event==0:
            if checkTimes == 0:
                t = threading.Thread(target=updateBFans, args=())  # creat thread
                t.setDaemon(True)
                t.start()
            print('draw1')
            image1 = Image.new("RGBA", (disp.width, disp.height), "black")
            draw = ImageDraw.Draw(image1)
            draw.text((20, 40), time.strftime("%Y-%m-%d", time.localtime()) ,font=newfont, fill="white")
            draw.text((20, 80), time.strftime("%H:%M:%S", time.localtime()) ,font=newfont, fill="white")
            draw.text((120, 150), u'粉丝数%s'%fans, font=smallfont, fill="#ffff00")
            draw.text((120, 186), u'新增粉丝数%s'%fansChange, font=smallfont, fill="#ff00ff")
            btv = Image.open("btv.png")
            btv = btv.resize((90, 90))
            image1.paste(btv, box=(20, 150))
            image1 = image1.rotate(180)
            image1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
            disp.ShowImage(image1, 0, 0)
            time.sleep(1)
            
            checkTimes += 1
            if checkTimes == 60:
                checkTimes = 0
        if event==1:
            if checkTimes == 0:
                t = threading.Thread(target=updateWeather(), args=())  # creat thread
                t.setDaemon(True)
                t.start()
            print('draw2')
            
            image1 = Image.new("RGBA", (disp.width, disp.height), "black")
            draw = ImageDraw.Draw(image1)
            draw.text((90, 150), u'温度: %s'%nowtemp, font=newfont, fill="#ff00ff")
            draw.text((110, 186), u'多云', font=newfont,fill="#ffff00")

            iconpath="icon/{}.png".format(icon)
            btv = Image.open(iconpath)
            btv = btv.resize((90, 90))
            image1.paste(btv, box=(100,50))
            image1 = image1.rotate(180)
            image1 = image1.transpose(Image.FLIP_LEFT_RIGHT)
            disp.ShowImage(image1, 0, 0)
            time.sleep(1)
           
            checkTimes += 1
            if checkTimes == 60:
                checkTimes = 0
        if event==2:
            if checkTimes == 0:
                t = threading.Thread(target=Showgif(), args=())  # creat thread
                t.setDaemon(True)
                t.start()
            print('draw3')
            
            gif_player = AnimatedGif(disp.ShowImage,Xstart=0,Ystart=0,width=240, height=240, folder=".")
            checkTimes += 1
            if checkTimes == 60:
                checkTimes = 0
       




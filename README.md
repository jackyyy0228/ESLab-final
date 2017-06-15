# ESLab-final

## Description
 - Use sensors to play Mario!
 - Mario URL : http://www.freemario.org/
 - 5 types of movement : right left Jump Down Fire
![Image of Homepage](https://github.com/jackyyy0228/ESLab-final/blob/master/homepage.png)
Demo video : 

## Setup for Raspberry pi 3
- I2C MPUX060

  (a) modify /etc/modules : add i2c-bcm2708
  
  (b) sudo apt-get install python-smbus i2c-tools git-core
  
  (c) sudo raspi-config，enable I2C
  
  (d) reboot
  
  tutorial : http://blogger.gtwang.org/2014/12/raspberry-pi-mpu6050-six-axis-gyro-accelerometer-1.html
  
- python
 ```
 sudo apt-get update
 sudo apt-get python-pip python-dev ipython
 sudo apt-get bluetooth libbluetooth-dev
 sudo pip install pybluez
 git clone https://github.com/jackyyy0228/ESLab-final
 ```
 
 - modify bluetooth address (of your PC) in client.py
 
 ```
 python client.py
 ```
## Setup for your PC
- install win32api
 
 ```
 sudo pip install pybluez PyUserInput
 git clone https://github.com/jackyyy0228/ESLab-final
 ```
- modify bluetooth address (of two raspberrypi3) in server.py

 ```
 python server.py
 ```
- open Mario http://www.freemario.org/

## Usage :
- Right : rotate rpi on your right hand to right
- Left :  rotate rpi on your right hand to left
- Down :  rotate rpi on your right hand to earth
- Jump :  move up rpi on your right hand 
- Fire :  move rpi on your left hand quickly
 

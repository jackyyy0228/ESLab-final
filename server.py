#Setup
#sudo pip install pybluez PyUserInput

import bluetooth
import threading
import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from data import *
server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 2
server_sock.bind(("",port))
server_sock.listen(2)

print("Waiting for connection")

berrydict ={'B8:27:EB:D2:75:3B':'right','B8:27:EB:A2:06:F1':'left'}

class echoThread(threading.Thread):
    def __init__ (self,sock,client_info,dire,syn):
        threading.Thread.__init__(self)
        self.sock = sock
        self.client_info = client_info
        self.dire = dire
        self.syn=syn
    def run(self):
        self.syn.set_connected(self.dire)
        try:
            while True:
                data = self.sock.recv(1024)
                if len(data) == 0: break
                data = package.from_string(data)
                #data.print_data()
                #print(data.get_norm_accel())
                self.syn.recv(data,self.dire)
        except IOError:
            pass
        self.sock.close()
        print(self.dire, ": disconnected")
        self.syn.set_closed(self.dire)
class jump(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.jump = False
    def run(self):
    	k = PyKeyboard()
    	try:
    		while True:
    			if self.jump:
    				k.press_key('z')
    				time.sleep(0.38)
    				k.release_key('z')
    				self.jump = False
    	except IOError:
            print('syn breaks down')
            exit(1)
    def set_jump(self):
    	self.jump = True

class syncronz(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.right = False
        self.left = False
        self.rightdata=''
        self.leftdata=''
    def run(self):
        try:
            allConnected = False
            while not allConnected:
                time.sleep(0.5)
                if not (self.right and self.left): continue
                if self.rightdata == '' or self.leftdata == '': continue
                allConnected = True
            k = PyKeyboard()
            r = 0
            l = 0
            d = 0
            f = 0
            j = jump()
            j.setDaemon(True)
            j.start()
            while True:
                if self.isRight(self.rightdata) and r == 0:
                    k.press_key(k.right_key)
                    r = 1
                elif r == 1 and not self.isRight(self.rightdata):
                    k.release_key(k.right_key)
                    r = 0
                if l == 0 and self.isLeft(self.rightdata) :
                    k.press_key(k.left_key)
                    l = 1
                elif l == 1 and not self.isLeft(self.rightdata):
                    k.release_key(k.left_key)
                    l = 0
               	if d == 0 and self.isDown(self.rightdata):
               		k.press_key(k.down_key)
               		d = 1
               	elif d == 1 and not self.isDown(self.rightdata):
               		k.release_key(k.down_key)
               		d = 0
               	if self.isJump(self.rightdata):
                    j.set_jump()
                if self.isFire(self.leftdata):
                    k.tap_key('x')
                time.sleep(0.005)
        except IOError:
            print('syn breaks down')
            exit(1)
    def set_connected(self,dire):
        if dire == 'right':
            self.right = True
        elif dire == 'left':
            self.left = True
    def set_closed(self,dire):
        if dire == 'right':
            self.right = False
        elif dire == 'left':
            self.left = False
    def recv(self,data,dire):
        if dire == 'right':
            self.rightdata = data
        elif dire == 'left':
            self.leftdata = data
    def isJump(self,data):
        if data.rota_z > 12:
            return True
        return False
    def isLeft(self,data):
        if data.rota_x < -30:
            return True
        return False
    def isRight(self,data):
    	# print data.rota_x
    	time.sleep(0.1)
        if data.rota_x > 30:
            return True
        return False
    def isDown(self,data):
        if data.rota_z < -40:
            return True
        return False
    def isFire(self,data):
        if data.get_norm_accel() > 2.0:
            return True
        return False

syn = syncronz()
syn.setDaemon(True)
syn.start()

while True:
    client_sock, client_info = server_sock.accept()
    print(berrydict[client_info[0]], " has connected ")
    echo = echoThread(client_sock, client_info,berrydict[client_info[0]],syn)
    echo.setDaemon(True)
    echo.start()
server_sock.close()
print('server is closed.')

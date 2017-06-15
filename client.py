import bluetooth
import time
import smbus
import math
from data import *

#bd_addr = '5C:F3:70:7F:24:BD' # ESlab
bd_addr = '18:CF:5E:6C:56:F9'

port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z, dist(x,y))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)


while True:
    '''
    print "------------------------------------------------"
    print "gyro data"
    print "---------"
    '''
    gyro_xout = read_word_2c(0x43) / 131
    gyro_yout = read_word_2c(0x45) / 131
    gyro_zout = read_word_2c(0x47) / 131
    '''
    print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout)
    print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout)
    print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout)

    print
    print "accelerometer data"
    print "------------------"
    '''
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    '''
    print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
    print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
    print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

    print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled) 
    print "z rotation: " , get_z_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    '''
    #Print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    pkg = package(float(gyro_xout), float(gyro_yout), float(gyro_zout),
                  float(accel_xout_scaled), float(accel_yout_scaled), float(accel_zout_scaled),
                  float(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)),
                  float(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)),
                  float(get_z_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)))
    #print 
    #print str(pkg.to_str())
    sock.send(str(pkg.to_str()))
    time.sleep(0.02)

sock.close()

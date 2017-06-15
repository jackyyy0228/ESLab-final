import math
class package():
    def __init__(self,a,b,c,d,e,f,g,h,i):
        self.gyro_x = a
        self.gyro_y = b
        self.gyro_z = c
        self.accel_x = d
        self.accel_y = e
        self.accel_z = f
        self.rota_x = g
        self.rota_y = h
        self.rota_z = i
        self.string = "{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f}".format(a,b,c,d,e,f,g,h,i)
    @classmethod
    def from_string(cls,string):
        a,b,c,d,e,f,g,h,i= [float(x)  for x in string.split(',')]
        return cls(a,b,c,d,e,f,g,h,i)
    def print_data(self):
        print
        print('gyro: x {:.4f} y {:.4f} z {:.4f}'.format(self.gyro_x,self.gyro_y,self.gyro_z))
        print('accel: x {:.4f} y {:.4f} z {:.4f}'.format(self.accel_x,self.accel_y,self.accel_z))
        print('rota: x {:.4f} y {:.4f} z {:.4f}'.format(self.rota_x,self.rota_y,self.rota_z))
    def to_str(self):
        return str(self.string)
    def get_norm_accel(self):
        return math.sqrt(self.accel_x*self.accel_x + self.accel_y*self.accel_y + self.accel_z*self.accel_z)

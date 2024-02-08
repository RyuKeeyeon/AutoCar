import time
from ctypes import *

class DC_motor:
    def __init__(self):
        self.swcarfunc = cdll.LoadLibrary('/home/pi/swcar_lib/librp_smartcar.so')
        self.swcarfunc.SIO_Init(0)
        self.swcarfunc.SIO_BrakeBLDC(1)
        self.swcarfunc.SIO_MaxMotorSpeed(100)
        self.motor_stop()

    def motor_move_forward(self, speed):
        self.swcarfunc.SIO_BrakeBLDC(1)
        self.swcarfunc.SIO_WriteBLDC(speed)

    def motor_move_reverse(self, speed):
        self.motor_move_forward(-speed)

    def motor_stop(self):
        self.swcarfunc.SIO_BrakeBLDC(0)
        self.swcarfunc.SIO_WriteBLDC(0)

class servo_motor:
    # 0은 우회전 100은 좌회전
    def __init__(self):
        self.swcarfunc = cdll.LoadLibrary('/home/pi/swcar_lib/librp_smartcar.so')
        self.center()

    def set_angle(self, angle):
        if angle < 0 or angle > 100:
            print("Angle must be between 0 and 100")
            return
        self.swcarfunc.SIO_WriteServo(100, angle)

    def center(self):
        self.set_angle(50)


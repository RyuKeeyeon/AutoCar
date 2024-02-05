import time
from ctypes import *


class car:

    def __init__(self):
        self.wirePIfunc = CDLL("/home/pi/WiringPi/wiringPi/libwiringPi.so.2.70", mode=RTLD_GLOBAL)
        self.swcarfunc = cdll.LoadLibrary('/home/pi/swcar_lib/librp_smartcar.so')
        self.swcarfunc.SIO_Init(0)
        self.swcarfunc.SIO_BrakeBLDC(1)
        self.swcarfunc.SIO_MaxMotorSpeed(100)

        self.motor_stop()
        self.servo_center()
        time.sleep(2)

    def motor_forward(self):
        speed = 50
        self.swcarfunc.SIO_BrakeBLDC(1)
        self.swcarfunc.SIO_WriteBLDC(speed)

    def motor_reverse(self):
        speed = -50
        self.swcarfunc.SIO_BrakeBLDC(1)
        self.swcarfunc.SIO_WriteBLDC(speed)

        self.sensor_dist_rear = 0
        self.sensor_pos_ir = 0

    def motor_stop(self):
        speed = 0
        self.swcarfunc.SIO_WriteBLDC(speed)
        self.swcarfunc.SIO_BrakeBLDC(0)

    def servo_left(self):
        self.swcarfunc.SIO_WriteServo(100, 90)

    def servo_right(self):
        self.swcarfunc.SIO_WriteServo(100, 10)

    def servo_center(self):
        self.swcarfunc.SIO_WriteServo(100, 50)

    def sensor_get_distance_US_FRONT(self):
        self.sensor_dist_front = self.swcarfunc.SIO_ReadDistUS(1)
        return self.sensor_dist_front

    def sensor_get_distance_US_REAR(self):
        self.sensor_dist_rear = self.swcarfunc.SIO_ReadDistUS(0)
        return self.sensor_dist_rear

    def sensor_get_position_IR(self):
        self.sensor_pos_ir = self.swcarfunc.SIO_ReadIR()
        return self.sensor_pos_ir


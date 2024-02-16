import time
from ctypes import *
import sys

class BLDCMotor:
    def __init__(self, swcar):
        self.swcar = swcar

    def init_motor(self):
        self.swcar.SIO_Init(0)
        self.swcar.SIO_MaxMotorSpeed(100)
        self.swcar.SIO_BrakeBLDC(1)

    def control_motor(self, speed):
        if 0<= speed <= 100:
            self.swcar.SIO_WriteBLDC(speed)
        else:
            self.swcar.SIO_WriteBLDC(speed)
            self.swcar.SIO_BrakeBLDC(0)

class ServoMotor:
    def __init__(self, swcar, channel=100):
        self.swcar = swcar
        self.channel = channel

    def control_motor(self, angle):
        self.swcar.SIO_WriteServo(self.channel, angle)


# 예제 사용법
# swcar_instance를 초기화하는 코드 필요
# bldc_motor = BLDCMotor(swcar_instance)
# bldc_motor.init_motor()
# bldc_motor.control_motor(50) # BLDC 모터를 50의 속도로 제어

# servo_motor = ServoMotor(swcar_instance)
# servo_motor.control_motor(30) # 서보 모터를 30도 각도로 제어

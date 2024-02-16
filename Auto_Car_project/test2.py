import time
from ctypes import *


WiringPi = CDLL("/home/pi/WiringPi/wiringPi/libwiringPi.so.2.70", mode=RTLD_GLOBAL)
swcar = cdll.LoadLibrary('/home/pi/swcar_lib/librp_smartcar.so')

class Motor:
    def __init__(self, swcar):
        self.swcar = swcar

    def control_motor(self, motor_status, speed, angle):
        self.swcar.SIO_Init(0)
        self.swcar.SIO_MaxMotorSpeed(100)
        self.swcar.SIO_BrakeBLDC(1)

        if motor_status == "FORWARD":
            self.swcar.SIO_WriteServo(100, angle)
            self.swcar.SIO_WriteBLDC(speed)
        elif motor_status == "REVERSE":
            self.swcar.SIO_WriteServo(100, angle)
            self.swcar.SIO_WriteBLDC(-speed)
        else:  # STOP
            self.swcar.SIO_WriteBLDC(0)
            self.swcar.SIO_BrakeBLDC(0)


swcar_instance = swcar

# MotorController 클래스의 인스턴스를 생성합니다.
motor_controller = Motor(swcar_instance)

# 3초 동안 전진
motor_controller.control_motor("FORWARD", 50, 50)
time.sleep(3)

# 3초 동안 후진
motor_controller.control_motor("REVERSE", 50, 50)
time.sleep(3)

# 정지
motor_controller.control_motor("STOP", 0, 0)

import time
from ctypes import *

class Motor:
    def __init__(self, swcar):
        self.swcar = swcar

    def control_motor(self, motor_status, speed, angle):

        self.swcar.SIO_Init(0)
        self.swcar.SIO_MaxMotorSpeed(100)
        self.swcar.SIO_BrakeBLDC(1)

        if (motor_status == "FORWARD"):
            self.swcar.SIO_WriteServo(100, -(angle - 50))
            self.swcar.SIO_WriteBLDC(speed)
        elif (motor_status == "REVERSE"):
            self.swcar.SIO_WriteServo(100, -(angle - 50))
            self.swcar.SIO_WriteBLDC(-(speed))
        else:
            self.swcar.SIO_WriteBLDC(0)

# example
# motor_controller = MotorController(swcar_instance)
# motor_controller.control_motor("FORWARD", 50, 30)

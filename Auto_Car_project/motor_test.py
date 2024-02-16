from ctypes import *
import time

# 라이브러리와 SWCar 인스턴스 초기화
WiringPi = CDLL("/home/pi/WiringPi/wiringPi/libwiringPi.so.2.70", mode=RTLD_GLOBAL)
swcar = cdll.LoadLibrary('/home/pi/swcar_lib/librp_smartcar.so')


class Motor:
    def __init__(self, swcar):
        self.swcar = swcar
        self.swcar.SIO_Init(0)
        self.swcar.SIO_MaxMotorSpeed(100)
        self.swcar.SIO_BrakeBLDC(1)

    def control_motor(self, motor_status, speed, angle):
        if motor_status == "FORWARD":
            self.swcar.SIO_WriteServo(30, angle)
            self.swcar.SIO_WriteBLDC(speed)
        elif motor_status == "REVERSE":
            self.swcar.SIO_WriteServo(30, angle)
            self.swcar.SIO_WriteBLDC(-speed)
        else:
            self.swcar.SIO_WriteBLDC(0)
            self.swcar.SIO_BrakeBLDC(0)


# 모터 인스턴스 생성
motor = Motor(swcar)

print('Press ctrl + c to terminate program')
print('Running Motor Test.')

iAngle = 0
iInc = 20
motor_status = "FORWARD"
while True:
    iAngle += iInc
    if iAngle > 100:
        iInc = -20
        motor_status = "Forward"
    if iAngle < 0:
        iInc = 20
        motor_status = "FORWARD"

    # 서보모터의 각도와 속도를 업데이트하여 모터 제어
    motor.control_motor(motor_status, 30, iAngle)  # 속도는 30으로 고정
    print("Motor Status:", motor_status, "| Angle:", iAngle)
    time.sleep(2)

import cv2
import os
import time
from ctypes import *
from Lane_recognition import *
# from Motor import *
from Video import *


# WiringPi 라이브러리 로드
WiringPi = CDLL("/home/pi/WiringPi/wiringPi/libwiringPi.so.2.70", mode=RTLD_GLOBAL)
swcar = cdll.LoadLibrary('/home/pi/swcar_lib/librp_smartcar.so')

# # WiringPi 라이브러리 초기화
# WiringPi.wiringPiSetup()

# swcar_instance = swcar
# # 객체 초기화
# bldc_motor = BLDCMotor(swcar_instance)
# bldc_motor.init_motor()
# servo_motor = ServoMotor(swcar_instance)
lane_recognition = LaneRecognition()
video_capture = VideoCapture()

# # Find ./data folder for labeling data
# try:
#     if not os.path.exists('./data'):
#         os.makedirs('./data')
# except OSError:
#     print("failed to make ./data folder")
#
# # Create video codec object. We use 'XVID' format for Raspberry pi.
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # Video write object for cropped frames
# video_orig_left = cv2.VideoWriter('./data/car_video_left.avi', fourcc, 20.0, (640, 120))
# video_orig_right = cv2.VideoWriter('./data/car_video_right.avi', fourcc, 20.0, (640, 120))


def calculate_servo_angle(angle_left, angle_right):
    """스티어링 각도를 계산하고 서보모터의 각도 범위로 환산하는 함수, 새로운 요구사항에 맞게 수정됨."""
    # 유효성 검사: angle_left와 angle_right가 유효한 숫자인지 확인
    if angle_left is None or angle_right is None or np.isnan(angle_left) or np.isnan(angle_right):
        return None  # 유효하지 않은 경우, None 반환

    final_angle = max(angle_left, angle_right)

    # 새로운 요구사항에 따른 servo_angle 계산
    if 60 <= final_angle <= 85:
        servo_angle = 50
    elif 30 <= final_angle < 60:
        servo_angle = 80
    elif final_angle < 30:
        servo_angle = 100
        print("final_angle error! : ", final_angle)
    elif 85 < final_angle <= 110:
        servo_angle = 30
    elif final_angle > 110:
        print("final_angle error! : ", final_angle)
        servo_angle = 0
    else:
        print ("final_angle error! : ",final_angle)
        servo_angle = 50
    return servo_angle

def process_frame(frame):
    """프레임 처리 및 차선 인식, 스티어링 각도 계산"""
    lanes, img_lane = lane_recognition.get_lane(frame)
    angle, img_angle = lane_recognition.get_steering_angle(img_lane, lanes)
    return angle, img_angle


for i in range(30):
    ret, left_cropped, right_cropped = video_capture.get_cropped_frames()
    if not ret:
        print("Camera error")
        continue

    angle_left, img_lane_left = process_frame(left_cropped)
    angle_right, img_lane_right = process_frame(right_cropped)

    if angle_left is not None and angle_right is not None and not np.isnan(angle_left) and not np.isnan(angle_right):
        servo_angle = calculate_servo_angle(angle_left, angle_right)
        if servo_angle is not None:
            print("Final steering angle:", (angle_left + angle_right) / 2)
            print("Servo motor angle:", servo_angle)
        else:
            print("Invalid servo angle calculated.")
    else:
        print("Can't find lane on either side...")

# Start motor
swcar.SIO_Init(0)
swcar.SIO_MaxMotorSpeed(100)
swcar.SIO_BrakeBLDC(1)

swcar.SIO_WriteBLDC(30)
swcar.SIO_WriteServo(100, servo_angle)
time.sleep(0.5)

while True:
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # ESC 키
        break

    ret, left_cropped, right_cropped = video_capture.get_cropped_frames()
    if not ret:
        print("Capture error")
        continue

    # video_orig_left.write(left_cropped)
    # video_orig_right.write(right_cropped)

    angle_left, img_lane_left = process_frame(left_cropped)
    angle_right, img_lane_right = process_frame(right_cropped)

    # angle_left와 angle_right가 None이 아니고, NaN이 아닌지 확인
    if angle_left is not None and angle_right is not None and not np.isnan(angle_left) and not np.isnan(angle_right):
        print("right motor angle!", angle_right)
        print("left motor angle!", angle_left)
        servo_angle = calculate_servo_angle(angle_left, angle_right)

        # servo_angle이 유효한지 확인 (calculate_servo_angle 수정 필요 없음, 이미 정수 반환을 보장함)
        if servo_angle is not None:  # calculate_servo_angle이 None을 반환하지 않도록 보장
            swcar.SIO_WriteServo(100, servo_angle)
            print("Servo motor angle!", servo_angle)
            time.sleep(0.5)
    else:
        print("Invalid or missing angle data.")

# 정지 명령도 loop 외부에 있어야 하며, servo_angle 값에 의존하지 않아야 합니다.
swcar.SIO_BrakeBLDC(0)

video_capture.release()
# video_orig_left.release()
# video_orig_right.release()
cv2.destroyAllWindows()

import cv2
import os
import time
from ctypes import *
from Lane_recognition import *
from Motor import *
from Video import *


# WiringPi 라이브러리 로드
WiringPi = CDLL("/home/pi/WiringPi/wiringPi/libwiringPi.so.2.70", mode=RTLD_GLOBAL)
swcar = cdll.LoadLibrary('/home/pi/swcar_lib/librp_smartcar.so')

# # WiringPi 라이브러리 초기화
# WiringPi.wiringPiSetup()

swcar_instance = swcar
# 객체 초기화
motor = Motor(swcar_instance)
lane_recognition = LaneRecognition()
video_capture = VideoCapture()

# Find ./data folder for labeling data
try:
    if not os.path.exists('./data'):
        os.makedirs('./data')
except OSError:
    print("failed to make ./data folder")

# Create video codec object. We use 'XVID' format for Raspberry pi.
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# Video write object for cropped frames
video_orig_left = cv2.VideoWriter('./data/car_video_left.avi', fourcc, 20.0, (640, 120))
video_orig_right = cv2.VideoWriter('./data/car_video_right.avi', fourcc, 20.0, (640, 120))

while True:
    ret, left_cropped, right_cropped = video_capture.get_cropped_frames()
    if ret:
        # Save cropped images
        video_orig_left.write(left_cropped)
        video_orig_right.write(right_cropped)

        # 왼쪽 크롭된 영상에서 차선 인식 및 스티어링 각도 계산
        lanes_left, img_lane_left = lane_recognition.get_lane(left_cropped)
        angle_left, img_angle_left = lane_recognition.get_steering_angle(img_lane_left, lanes_left)

        # 오른쪽 크롭된 영상에서 차선 인식 및 스티어링 각도 계산
        lanes_right, img_lane_right = lane_recognition.get_lane(right_cropped)
        angle_right, img_angle_right = lane_recognition.get_steering_angle(img_lane_right, lanes_right)

        if angle_left is not None and angle_right is not None:
            final_angle = (angle_left + angle_right) / 2
            # 스티어링 각도를 서보모터의 각도 범위로 환산
            servo_angle = ((final_angle - 60) * (100 - 0) / (120 - 60)) + 0

            # 범위 검사 로직 추가
            if servo_angle < 0:
                servo_angle = 0
            elif servo_angle > 100:
                servo_angle = 100

        # 스티어링 각도가 유효한 경우에만 모터 제어
        if servo_angle is not None:
            # Start motor - 이 호출은 servo_angle가 유효한 경우에만 실행됨
            print("Final steering angle:", final_angle)
            print("Servo motor angle:", servo_angle)

    else:
        print("cap error")


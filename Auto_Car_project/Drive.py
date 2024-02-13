import cv2
import os
import time
from ctypes import *
from Lane_recognition import *
from Motor import *
from Video import *

# WiringPi 라이브러리 로드
WiringPi = CDLL("/home/pi/WiringPi/wiringPi/libwiringPi.so.2.70", mode=RTLD_GLOBAL)

# WiringPi 라이브러리 초기화
WiringPi.wiringPiSetup()

# 객체 초기화
motor = Motor()
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

for i in range(30):
    ret, left_cropped, right_cropped = video_capture.get_cropped_frames()
    if ret:
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

            print("Final steering angle:", final_angle)
            print("Servo motor angle:", servo_angle)
        else:
            print("Can't find lane on either side...")
            servo_angle = 50

    else:
        print("Camera error")
        servo_angle = 50

# Start motor
motor.control_motor("FORWARD", 100, servo_angle)
while True:
    ret, left_cropped, right_cropped = video_capture.get_cropped_frames()
    if ret:
        # Save cropped images
        video_orig_left.write(left_cropped)
        video_orig_right.write(right_cropped)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 종료 조건
            break
    else:
        print("cap error")

motor.control_motor("STOP",0,50) # 모터 정지
video_capture.release()
video_orig_left.release()
video_orig_right.release()
cv2.destroyAllWindows()

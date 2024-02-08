import cv2
import os
import time
from Lane_recognition import LaneRecognition
from Motor import servo_motor, DC_motor
from Video import VideoCapture

# 객체 초기화
servo = servo_motor()
lane_recognition = LaneRecognition()
motor = DC_motor()
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

# Prepare real starting
for i in range(30):
    ret, left_cropped, right_cropped = video_capture.get_cropped_frames()
    if ret:
        # 왼쪽과 오른쪽 크롭된 영상에서 각각 차선 인식 및 스티어링 각도 계산
        _, angle_left = lane_recognition.process_frame(left_cropped)
        _, angle_right = lane_recognition.process_frame(right_cropped)

        # 두 각도의 평균 계산하여 최종 스티어링 각도 결정
        if angle_left is not None and angle_right is not None:
            final_angle = (angle_left + angle_right) / 2
            print("Final steering angle:", final_angle)
            servo.set_angle(final_angle)  # 서보 모터 각도 설정
        else:
            print("Can't find lane on either side...")
    else:
        print("Camera error")

# Start motor
motor.motor_move_forward(10)
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

motor.motor_stop()  # 모터 정지
video_capture.release()
video_orig_left.release()
video_orig_right.release()
cv2.destroyAllWindows()

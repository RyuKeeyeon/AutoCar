import cv2
from Lane_recognition import *# Lane_recognition.py 파일에서 클래스를 임포트

# 이미지 파일을 읽어옵니다. 실제 경로로 대체하세요.
frame = cv2.imread('path/to/your/image.jpg')

# LaneRecognition 클래스의 인스턴스를 생성합니다.
lane_recognition = LaneRecognition()

# 프레임 처리를 수행합니다. 이 함수는 수정된 이미지와 스티어링 각도를 반환합니다.
processed_frame, steering_angle = lane_recognition.process_frame(frame)

# 결과 이미지를 화면에 표시합니다.
cv2.imshow('Processed Frame', processed_frame)

# 스티어링 각도를 출력합니다.
print('Steering Angle:', steering_angle)

# cv2.waitKey() 함수를 호출하여 이미지 윈도우가 즉시 닫히지 않도록 합니다.
cv2.waitKey(0)

# 모든 윈도우를 정리합니다.
cv2.destroyAllWindows()

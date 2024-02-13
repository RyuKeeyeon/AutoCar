import cv2
from Lane_recognition import *
from matplotlib import pyplot as plt

def test_lane_recognition(image_path):
    # 이미지 불러오기
    frame = cv2.imread(image_path)
    if frame is None:
        print("Image not found or unable to read.")
        return

    # LaneRecognition 인스턴스 생성 및 메서드 호출
    lane_recognition = LaneRecognition()
    lane_lines, processed_frame = lane_recognition.get_lane(frame)
    steering_angle, heading_image = lane_recognition.get_steering_angle(processed_frame, lane_lines)

    # 결과 이미지 시각화
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    if heading_image is not None:
        plt.imshow(cv2.cvtColor(heading_image, cv2.COLOR_BGR2RGB))
        plt.title(f'Heading Image with Steering Angle: {steering_angle}')
    else:
        print("No heading image generated.")
    plt.show()

# 실제 이미지 파일 경로로 변경해야 함
test_image_path = r'C:\Auto_Car\Auto_Car_project\left_cropped.jpg'
test_lane_recognition(test_image_path)

import cv2
from Lane_recognition import *
from matplotlib import pyplot as plt
# VideoCapture 클래스 정의는 여기에 포함되어 있습니다.
class VideoCapture:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    def get_cropped_frames(self):
        ret, img_org = self.cap.read()
        if ret:
            # Split the image into left and right
            left_image = img_org[:, :640]  # Left side of the image
            right_image = img_org[:, 640:]  # Right side of the image

            # Crop the bottom half of each side
            height = left_image.shape[0]
            left_cropped = left_image[int(height/1.5):, :]
            right_cropped = right_image[int(height/1.5):, :]
            return True, left_cropped, right_cropped
        else:
            return False, None, None

    def release(self):
        self.cap.release()
def main():
    video_capture = VideoCapture()  # VideoCapture 인스턴스 생성

    while True:
        ret, left_cropped, right_cropped = video_capture.get_cropped_frames()  # 자른 프레임 가져오기
        if not ret:
            print("Capture error")
            break  # 캡처에 실패하면 루프 종료

        # 왼쪽과 오른쪽 이미지를 수평으로 합치기
        combined_image = cv2.hconcat([left_cropped, right_cropped])

        # 합쳐진 이미지 표시
        cv2.imshow("Cropped Frames", combined_image)

        # 'ESC' 키로 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break

    video_capture.release()  # 자원 해제
    cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기

if __name__ == "__main__":
    main()

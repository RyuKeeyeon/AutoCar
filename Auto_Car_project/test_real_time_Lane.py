import cv2
from Lane_recognition import *


class RealTimeLaneRecognition:
    def __init__(self):
        self.lane_recognition = LaneRecognition()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def process_frame(self, frame):
        # 차선 인식과 조향 각도 계산
        lane_lines, processed_frame = self.lane_recognition.get_lane(frame)
        steering_angle, heading_image = self.lane_recognition.get_steering_angle(processed_frame, lane_lines)

        return steering_angle, heading_image

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Frame processing
            steering_angle, heading_image = self.process_frame(frame)

            # Display the processed frame
            cv2.imshow('Heading Image with Steering Angle', heading_image if heading_image is not None else frame)

            # ESC 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    real_time_lane_recognition = RealTimeLaneRecognition()
    real_time_lane_recognition.run()

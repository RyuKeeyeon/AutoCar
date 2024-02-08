import cv2

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

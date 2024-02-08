
import cv2
import numpy as np
import logging
import math

class LaneRecognition:
    def __init__(self):
        self.curr_steering_angle = 90

    def detect_edges(self, frame):
        # filter for lane lines
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Assuming lane lines are white
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        edges = cv2.Canny(mask, 200, 400)
        return edges

    def region_of_interest(self, edges):
        height, width = edges.shape
        mask = np.zeros_like(edges)
        polygon = np.array([[
            (0, height * 0.6),
            (width, height * 0.6),
            (width, height),
            (0, height),
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_image = cv2.bitwise_and(edges, mask)
        return masked_image

    def detect_lane_lines(self, frame):
        edges = self.detect_edges(frame)
        cropped_edges = self.region_of_interest(edges)
        lines = cv2.HoughLinesP(cropped_edges, 1, np.pi/180, 50, np.array([]), minLineLength=100, maxLineGap=50)
        return lines

    def compute_steering_angle(self, frame, lines):
        if len(lines) == 0:
            return self.curr_steering_angle
        line_image = np.zeros_like(frame)
        for line in lines:
            for x1, y1, x2, y2 in line:
                angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        curr_steering_angle = angle + 90
        return curr_steering_angle

    def display_heading_line(self, frame, steering_angle):
        heading_image = np.zeros_like(frame)
        height, width, _ = frame.shape
        steering_angle_radian = steering_angle / 180.0 * np.pi
        x1 = int(width / 2)
        y1 = height
        x2 = int(x1 - height / 2 / np.tan(steering_angle_radian))
        y2 = int(height / 2)
        cv2.line(heading_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
        heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)
        return heading_image

    def process_frame(self, frame):
        lines = self.detect_lane_lines(frame)
        steering_angle = self.compute_steering_angle(frame, lines)
        heading_image = self.display_heading_line(frame, steering_angle)
        return heading_image, steering_angle

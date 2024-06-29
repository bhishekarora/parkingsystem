import re 
import cv2
import easyocr
import requests
import time
import torch
from datetime import datetime

class TailNumberExtractor:
    def __init__(self, rtsp_url, external_system_url, gpu=True):
        self.rtsp_url = rtsp_url
        self.external_system_url = external_system_url
        self.use_gpu = gpu and torch.cuda.is_available()
        self.reader = easyocr.Reader(['en'], gpu=self.use_gpu)

    def capture_and_process(self, skip_frames=10, resize_factor=0.5):
        print(f"Connecting to RTSP stream at {self.rtsp_url}...")
        cap = cv2.VideoCapture(self.rtsp_url)

        if not cap.isOpened():
            print(f"Error: Unable to open video stream at {self.rtsp_url}")
            return

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            frame_count += 1

            if not ret:
                print("Error: Unable to read frame from stream")
                break

            if frame_count % skip_frames != 0:
                continue

            print(f"Processing frame {frame_count}...")
            # Resize frame to improve OCR speed
            frame_resized = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)
            gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

            # Use EasyOCR to detect text
            result = self.reader.readtext(gray)

            print(f"OCR result for frame {frame_count}: {result}")
            for (bbox, text, prob) in result:
                if prob > 0.9:  # Adjust probability threshold as needed
                    if self.is_valid_tail_number(text):
                        print(f"Detected Flight: '{text}' with probability: {prob}")

                        # Calculate text size in the original frame dimensions
                        bbox_original = [(int(point[0] / resize_factor), int(point[1] / resize_factor)) for point in bbox]
                        text_width = bbox_original[1][0] - bbox_original[0][0]
                        text_height = bbox_original[2][1] - bbox_original[0][1]
                        if text_height > 50:  # Example threshold for text size
                            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(f"Parking Charges started at {current_time}")
                            self.post_to_external_system(text)
                            # Draw bounding box and text on the frame for visual confirmation
                            frame = cv2.rectangle(frame, tuple(bbox_original[0]), tuple(bbox_original[2]), (0, 255, 0), 2)
                            frame = cv2.putText(frame, text, (bbox_original[0][0], bbox_original[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                            # Resize the window for display
                            display_frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
                            cv2.imshow('Video Frame', display_frame)

                            # Wait for any key press and then exit
                            print("Press any key to exit...")
                            cv2.waitKey(0)
                            cap.release()
                            cv2.destroyAllWindows()
                            return

        cap.release()
        cv2.destroyAllWindows()

    def is_valid_tail_number(self, text):
        # Define the regex pattern for tail number format XX-XXX
        pattern = r'^[A-Z0-9]{2}-[A-Z0-9]{3}$'
        return bool(re.match(pattern, text))

    def post_to_external_system(self, text):
        data = {'tail_number': text}
        print(f"Posting data to billing system: {data}")
        response = requests.post(self.external_system_url, json=data)
        if response.status_code == 200:
            print(f"Successfully posted tail number: {text} to AMS")
        else:
            print(f"Failed to post tail number: {text}, Status Code: {response.status_code}, Response: {response.text}")

# Usage
if __name__ == "__main__":
    rtsp_url = 'rtsp://localhost:8554/live.stream'
    external_system_url = 'http://localhost:5000/ams'
    extractor = TailNumberExtractor(rtsp_url, external_system_url, gpu=True)
    extractor.capture_and_process(skip_frames=10, resize_factor=0.5)

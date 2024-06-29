import cv2
import easyocr
import re
import torch

class TailNumberExtractor:
    def __init__(self, video_source, gpu=True):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        self.use_gpu = gpu and torch.cuda.is_available()
        self.reader = easyocr.Reader(['en'], gpu=self.use_gpu)  # Initialize EasyOCR reader with GPU support if available

    def read_frames_and_ocr(self, skip_frames=10, resize_factor=0.5):
        frame_count = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % skip_frames != 0:
                continue

            # Resize frame to improve OCR speed
            frame_resized = cv2.resize(frame, (0, 0), fx=resize_factor, fy=resize_factor)
            gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)

            # Use EasyOCR to detect text
            result = self.reader.readtext(gray)

            print(f"OCR result for frame {frame_count}: {result}")
            for (bbox, text, prob) in result:
                print(f"Detected Flight: '{text}' with probability: {prob}")
                if prob > 0.9:  # Adjust probability threshold as needed
                    if self.is_valid_tail_number(text):
                        # Calculate text size in the original frame dimensions
                        bbox_original = [(int(point[0] / resize_factor), int(point[1] / resize_factor)) for point in bbox]
                        text_width = bbox_original[1][0] - bbox_original[0][0]
                        text_height = bbox_original[2][1] - bbox_original[0][1]
                        if text_height > 50:  # Example threshold for text size
                            print("send to sap")
                            # Draw bounding box and text on the frame for visual confirmation
                            frame = cv2.rectangle(frame, tuple(bbox_original[0]), tuple(bbox_original[2]), (0, 255, 0), 2)
                            frame = cv2.putText(frame, text, (bbox_original[0][0], bbox_original[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show the frame (optional, for visual confirmation)
            cv2.imshow('Video Frame', frame)
            cv2.waitKey(1)

        self.cap.release()
        cv2.destroyAllWindows()

    def is_valid_tail_number(self, text):
        # Define the regex pattern for tail number format XX-XXX
        pattern = r'^[A-Z0-9]{2}-[A-Z0-9]{3}$'
        return bool(re.match(pattern, text))

if __name__ == "__main__":
    # Provide the path to your video file
    video_source = "hangar.mp4"
    tail_number_extractor = TailNumberExtractor(video_source, gpu=True)
    tail_number_extractor.read_frames_and_ocr(skip_frames=10, resize_factor=0.5)

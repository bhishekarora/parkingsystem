import subprocess
import time
import signal
import os

class RTSPStreamer:
    def __init__(self, video_file, rtsp_url):
        self.video_file = video_file
        self.rtsp_url = rtsp_url
        self.process = None

    def start_stream(self):
        # Command to start the RTSP stream using ffmpeg
        command = [
            'ffmpeg',
            '-re',
            '-stream_loop', '-1',
            '-i', self.video_file,
            '-c:v', 'libx264',
            '-f', 'rtsp',
            self.rtsp_url
        ]

        try:
            # Start the ffmpeg process
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Started streaming {self.video_file} to {self.rtsp_url}")
        except Exception as e:
            print(f"Failed to start ffmpeg process: {e}")

    def stop_stream(self):
        if self.process:
            try:
                # Send the SIGTERM signal to the ffmpeg process
                self.process.send_signal(signal.SIGTERM)
                self.process.wait()
                print("Stopped the RTSP stream")
            except Exception as e:
                print(f"Failed to stop ffmpeg process: {e}")

    def read_ffmpeg_output(self):
        if self.process:
            try:
                while True:
                    output = self.process.stderr.readline()
                    if output == '' and self.process.poll() is not None:
                        break
                    if output:
                        print(f"FFmpeg output: {output.strip()}")
            except Exception as e:
                print(f"Error reading ffmpeg output: {e}")

if __name__ == "__main__":
    video_file = 'hangar.mp4'
    rtsp_url = 'rtsp://localhost:8554/mystream'

    streamer = RTSPStreamer(video_file, rtsp_url)
    streamer.start_stream()

    try:
        while True:
            time.sleep(1)
            streamer.read_ffmpeg_output()  # Read ffmpeg output periodically for debugging
    except KeyboardInterrupt:
        streamer.stop_stream()

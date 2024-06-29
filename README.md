# Tail Number Extractor with AMS Interface

This project captures video frames from an RTSP stream, extracts text using OCR, and posts detected tail numbers to an external system (simulated using a Flask-based API).

## Project Structure

- `ams_server.py`: Flask API that simulates the external system.
- `tail_number_extractor.py`: Script that captures video frames, performs OCR, and posts detected tail numbers to the Flask API.

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**

    ```sh
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. **Create a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Start the Flask API

1. **Run the Flask API:**

    ```sh
    python ams_server.py
    ```

    This will start the Flask API on port 5000, which listens for tail number POST requests.

### Run the Tail Number Extractor

1. **Run the Tail Number Extractor script:**

    ```sh
    python tail_number_extractor.py
    ```

    This script will connect to the RTSP stream, process the video frames to detect tail numbers, and post the detected tail numbers to the Flask API.

## Configuration

- **RTSP URL:** Set the RTSP URL in `tail_number_extractor.py` file.
- **External System URL:** Set the URL of the Flask API in `tail_number_extractor.py` file.

## Requirements

- `ams_server.py`:
  - Flask
- `tail_number_extractor.py`:
  - OpenCV
  - EasyOCR
  - Requests
  - Torch (optional, for GPU support)

## Requirements File

The `requirements.txt` file lists all the dependencies needed to run the project. 

## License

This project is licensed under the MIT License.

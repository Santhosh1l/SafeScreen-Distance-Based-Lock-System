
# Safedistane based Lock System

## Overview

This project is designed to enhance user safety by monitoring the distance between the user's face and the computer screen using a webcam. If the user gets too close to the screen, the system warns the user and automatically locks the computer if the user fails to move back within a safe distance.

## Features

- **Real-Time Face Detection:** The system uses OpenCV's Haar Cascade classifier to detect faces in real time.
- **Distance Calculation:** It calculates the distance of the user's face from the camera using the perceived width of the face.
- **Proximity Alert:** If the user is too close to the screen, a warning message is displayed.
- **Automatic Lock:** If the user remains too close to the screen, the system automatically locks the computer.
- **Brightness Adjustment:** The system automatically adjusts the brightness of the webcam feed if the lighting conditions are poor.
- **Configurable Parameters:** You can adjust the known face width, camera focal length, danger distance, and brightness threshold according to your setup.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- OpenCV (`cv2`)
- NumPy

You can install the required libraries using pip:

```sh
pip install opencv-python-headless numpy
```

## How It Works

1. **Face Detection:** The system captures video from the webcam and converts each frame to grayscale for face detection.
2. **Brightness Adjustment:** If the average brightness of the frame is below a certain threshold, the brightness is increased.
3. **Distance Measurement:** The width of the detected face is used to estimate the distance from the camera.
4. **Alert & Lock:** If the face is too close (within the danger distance), a warning message is shown. If the user does not move back, the system locks the computer.
5. **Camera Timing:** The camera remains on for a set duration, and then turns off for a brief period before restarting.

## Usage

1. **Run the Script:**
   To start the application, run the script using Python:
   ```sh
   python face_distance_proximity_alert.py
   ```

2. **Quit the Application:**
   Press `q` to quit the application manually.

## Configuration

You can adjust the following constants in the script to match your setup:

- `KNOWN_WIDTH`: Average width of a face in mm.
- `FOCAL_LENGTH`: Focal length of the camera (needs calibration).
- `DANGER_DISTANCE`: Distance in mm at which the system will trigger the warning and lock.
- `BRIGHTNESS_THRESHOLD`: Threshold for increasing brightness in low light conditions.
- `ON_DURATION`: Duration in seconds for which the camera stays on.
- `OFF_DURATION`: Duration in seconds for which the camera stays off between cycles.

## Platform Compatibility

The locking mechanism is compatible with:

- **Windows:** Uses `LockWorkStation`.
- **macOS:** Uses `pmset displaysleepnow` (puts the display to sleep, which locks the screen).
- **Linux (GNOME):** Uses `gnome-screensaver-command -l`.

## License

This project is licensed under the MIT License.

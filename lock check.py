import cv2
import numpy as np
import time
import os
import platform

# Constants
KNOWN_WIDTH = 160  # Average width of a face in mm (you may need to adjust this)
FOCAL_LENGTH = 600  # Focal length of the camera, this needs to be calibrated
DANGER_DISTANCE = 400  # Distance in mm to warn the user to move back
BRIGHTNESS_THRESHOLD = 100  # Threshold to decide if brightness needs to be increased
ON_DURATION = 600  # Camera on duration in seconds (10 minutes)
OFF_DURATION = 10   # Camera off duration in seconds (10 sec)

lock_triggered = False

def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    v = cv2.add(v, value)
    v[v > 255] = 255
    
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def lock_computer():
    global lock_triggered
    lock_triggered = True
    if platform.system() == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif platform.system() == "Darwin":
        os.system("pmset displaysleepnow")  # For macOS (locks screen after sleep)
    elif platform.system() == "Linux":
        os.system("gnome-screensaver-command -l")  # For GNOME (locks screen)
    else:
        print("Locking mechanism not supported for this OS")

def main():
    global lock_triggered
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    vidcap = cv2.VideoCapture(0)
    
    while True:
        lock_triggered = False
        # Turn on the camera
        start_time = time.time()
        while time.time() - start_time < ON_DURATION and not lock_triggered:
            success, frame = vidcap.read()
            if not success:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)
            
            if avg_brightness < BRIGHTNESS_THRESHOLD:
                frame = increase_brightness(frame, value=60)
            
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))
            
            warning_message = "Safe distance."
            for (x, y, w, h) in faces:
                distance = distance_to_camera(KNOWN_WIDTH, FOCAL_LENGTH, w)
                if distance < DANGER_DISTANCE:
                    warning_message = "Go back! Your face is too close."
                    lock_computer()  # Lock the computer if face is too close
                    break
            
            height, width = frame.shape[:2]
            cv2.putText(frame, warning_message, (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255) if "Go back" in warning_message else (0, 255, 0), 2)
            
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        vidcap.release()
        cv2.destroyAllWindows()
        
        # Turn off the camera
        if lock_triggered:
            print("Screen locked. Camera off.")
            break
        else:
            print("Camera off. Waiting for {} seconds...".format(OFF_DURATION))
            time.sleep(OFF_DURATION)

if __name__ == "__main__":
    main()

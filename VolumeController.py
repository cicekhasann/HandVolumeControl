import cv2
import math
import numpy as np
import alsaaudio
from HandDetector import HandDetector

handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)

# Volume related initializations
m = alsaaudio.Mixer()

def main():
    while True:
        status, image = webcamFeed.read()
        image = cv2.flip(image, 1)
        handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)

        if len(handLandmarks) != 0:
            x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
            x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
            length = math.hypot(x2 - x1, y2 - y1)
            print(length)

            # Hand range(length): 50-250
            # Volume Range: 0-100 (for alsaaudio)

            volumeValue = np.interp(length, [50, 250], [0, 100])  # Convert length to volume range
            set_system_volume(volumeValue)

            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

        cv2.imshow("Volume", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcamFeed.release()
    cv2.destroyAllWindows()


def set_system_volume(volume_value):
    m.setvolume(int(volume_value))

if __name__ == "__main__":
    main()

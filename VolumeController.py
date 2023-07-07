import cv2
import math
import numpy as np
import platform
from HandDetector import HandDetector

handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)

if platform.system() == 'Windows':
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    # Volume related initializations
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # print(volume.GetVolumeRange()) --> (-65.25, 0.0)
elif platform.system() == 'Linux':
    import alsaaudio

    # Volume related initializations
    m = alsaaudio.Mixer()

def main():
    while True:
        status, image = webcamFeed.read()
        image = cv2.flip(image,1)
        handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)

        if(len(handLandmarks) != 0):
            #for volume control we need 4th and 8th landmark
            #details: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
            x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
            x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
            length = math.hypot(x2-x1, y2-y1)
            print(length)

            #Hand range(length): 50-250
            #Volume Range: (-65.25, 0.0) for Windows, 0-100 for Linux

            if platform.system() == 'Windows':
                volumeValue = np.interp(length, [50, 250], [-65.25, 0.0]) #coverting length to proportionate to volume range
                volume.SetMasterVolumeLevel(volumeValue, None)
            elif platform.system() == 'Linux':
                volumeValue = np.interp(length, [50, 250], [0, 100]) #coverting length to proportionate to volume range
                set_system_volume(volumeValue)

            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

        cv2.imshow("Volume", image)
        # cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcamFeed.release()
    cv2.destroyAllWindows()

def set_system_volume(volume_value):
    m.setvolume(int(volume_value))

if __name__ == "__main__":
    main()

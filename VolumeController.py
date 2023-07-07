from HandDetector import HandDetector

import cv2
import math
import numpy as np
import platform
class VolumeController:
    def __init__(self, webcam):
        self.webcamFeed = webcam
        self.handDetector = HandDetector(min_detection_confidence=0.7)
        self.volume_control = self.initialize_volume_control()

    def initialize_volume_control(self):
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
            return volume
        elif platform.system() == 'Linux':
            import alsaaudio

            # Volume related initializations
            return alsaaudio.Mixer()

    def run(self):
        while True:
            status, image = self.webcamFeed.read()
            image = cv2.flip(image, 1)
            handLandmarks = self.handDetector.findHandLandMarks(image=image, draw=True)

            if len(handLandmarks) != 0:
                x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
                x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
                length = math.hypot(x2 - x1, y2 - y1)
                print(length)

                # Hand range(length): 50-250
                # Volume Range: (-65.25, 0.0) for Windows, 0-100 for Linux

                if platform.system() == 'Windows':
                    volumeValue = np.interp(length, [50, 250], [-65.25, 0.0])  # converting length to proportionate to volume range
                    self.volume_control.SetMasterVolumeLevel(volumeValue, None)
                elif platform.system() == 'Linux':
                    volumeValue = np.interp(length, [50, 250], [0, 100])  # converting length to proportionate to volume range
                    self.set_system_volume(volumeValue)

                cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cv2.imshow("Volume", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.webcamFeed.release()
        cv2.destroyAllWindows()

    def set_system_volume(self, volume_value):
        self.volume_control.setvolume(int(volume_value))


import cv2
from VolumeController import VolumeController

def main():
    webcamFeed = cv2.VideoCapture(0)
    volumeController = VolumeController(webcamFeed)
    volumeController.run()

if __name__ == "__main__":
    main()

from PIL import Image
import cv2
import numpy as np

class ImageConverter:
    def __init__(self):
        pass

    def pilToCv2(self, pilImage):
        return cv2.cvtColor(np.array(pilImage), cv2.COLOR_RGB2BGR)


    def cv2toPil(self, cv2Image):
        cv2Temp = cv2.cvtColor(cv2Image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(cv2Temp)

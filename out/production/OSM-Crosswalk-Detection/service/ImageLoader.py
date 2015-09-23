import cv2
import httplib2
import matplotlib as plt


class ImageLoader:


    def __init__(self):
        self.LINK = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/47.2246376,8.8178977/19/?key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq'



    def loadImage(self):
        resp, content = httplib2.Http().request(self.LINK)
        return content

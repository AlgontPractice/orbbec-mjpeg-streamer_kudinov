import logging
import cv2
import asyncio

import numpy as np


logger = logging.getLogger('orbbec-mjpeg-streamer')


class Scanner:

    def __init__(self, video_params: dict):
        self._video_params = video_params
        self.colrCap = None
        self.depthCap = None

    async def init_device(self):
        # TODO: метод, в котором реализуем подключение к камере с помощью библиотеки opencv-python
        self.depthCap = cv2.VideoCapture(cv2.CAP_OPENNI2_ASTRA)
        self.colorCap = cv2.VideoCapture(1)


        if not (self.depthCap.isOpened()):
            raise Exception()

    async def image_grabber(self, app):
        while True:
        # TODO: метод, в котором мы получаем кадры с камеры и сохраняем их в переменную app['frame'] в формате jpg
            self.colorCap.grab()
            self.depthCap.grab()

            depthStatus, depthMap = self.depthCap.retrieve(cv2.CAP_OPENNI_DEPTH_MAP)
            clrStatus, frame = self.colorCap.retrieve()
            minimal = np.array(depthMap).max()
            min_img = np.zeros((512,512,3), np.uint8)
            cv2.putText(min_img, str(minimal), (10,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 2)

            depthMap = depthMap.astype(np.uint8)
            if not (clrStatus):
                raise Exception()


            
            app['frame'] = cv2.imencode('.jpg', frame)[1]
            app['depthmap'] = cv2.imencode('.jpg', depthMap)[1]
            app['minimal'] = cv2.imencode('.jpg', min_img)[1]

            await asyncio.sleep(1/self._video_params['fps'])

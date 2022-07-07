import logging
import cv2
import asyncio

import numpy as np


logger = logging.getLogger('orbbec-mjpeg-streamer')


class Scanner:

    def __init__(self, video_params: dict):
        self._video_params = video_params
        self.colorCap = None
        # self.depthCap = None

    async def init_device(self):
        # TODO: метод, в котором реализуем подключение к камере с помощью библиотеки opencv-python
        self.depthCap = cv2.VideoCapture(cv2.CAP_OPENNI2_ASTRA)
        self.colorCap = cv2.VideoCapture(0)
        self.colorCap.set(cv2.CAP_PROP_FRAME_WIDTH, self._video_params['width'])
        self.colorCap.set(cv2.CAP_PROP_FRAME_HEIGHT, self._video_params['height'])
        self.colorCap.set(cv2.CAP_PROP_FPS, self._video_params['fps'])
        self.colorCap.set(cv2.CAP_PROP_CONTRAST, self._video_params['contrast'])
        self.colorCap.set(cv2.CAP_PROP_SATURATION, self._video_params['saturation'])
        self.colorCap.set(cv2.CAP_PROP_HUE, self._video_params['hue'])
        self.colorCap.set(cv2.CAP_PROP_HUE, self._video_params['hue'])
        self.colorCap.set(cv2.CAP_PROP_GAIN, self._video_params['gain'])
        self.colorCap.set(cv2.CAP_PROP_WB_TEMPERATURE, self._video_params['white_balance_temperature'])
        self.colorCap.set(cv2.CAP_PROP_SHARPNESS, self._video_params['sharpness'])
        self.colorCap.set(cv2.CAP_PROP_BACKLIGHT, self._video_params['backlight_compensation'])
        self.colorCap.set(cv2.CAP_PROP_AUTO_EXPOSURE, self._video_params['exposure_auto'])
        self.colorCap.set(cv2.CAP_PROP_EXPOSURE, self._video_params['exposure_absolute'])

        cv2.samples.addSamplesDataSearchPath('C:\\Users\\tri\\Documents\\projects\\PRAKTIKA2022\\opencv_samples')
        self.Cascade = cv2.CascadeClassifier()
        self.Cascade.load(cv2.samples.findFile('haarcascade_frontalface_alt.xml'))
        if self.Cascade.empty():
            raise Exception()


        if not (self.colorCap.isOpened()):
            raise Exception()

    async def image_grabber(self, app):
        while True:
        # TODO: метод, в котором мы получаем кадры с камеры и сохраняем их в переменную app['frame'] в формате jpg
            # self.colorCap.grab()
            # self.depthCap.grab()

            # depthStatus, depthMap = self.depthCap.retrieve(cv2.CAP_OPENNI_DEPTH_MAP)
            # clrStatus, frame = self.colorCap.retrieve()
            # minimal = int(np.array(depthMap).max())
            # app['minimal'] = minimal
            # depthMap = depthMap.astype(np.uint8)
            clrStatus, frame = self.colorCap.read()
            
            if not (clrStatus):
                raise Exception()

            
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.equalizeHist(frame_gray)
            recs = np.empty(0, 'int32')
            recs = self.Cascade.detectMultiScale(frame_gray)
            for (x, y, w, h) in recs:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.imwrite('recognitions/face.jpg', frame)


            app['frame'] = cv2.imencode('.jpg', frame)[1]
            # app['depthmap'] = cv2.imencode('.jpg', depthMap)[1]
            

            await asyncio.sleep(1/self._video_params['fps'])

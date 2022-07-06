import logging
import cv2
import asyncio


logger = logging.getLogger('orbbec-mjpeg-streamer')


class Scanner:

    def __init__(self, video_params: dict):
        self._video_params = video_params
        self.cap = None

    async def init_device(self):
        # TODO: метод, в котором реализуем подключение к камере с помощью библиотеки opencv-python
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception()

    async def image_grabber(self, app):
        while True:
        # TODO: метод, в котором мы получаем кадры с камеры и сохраняем их в переменную app['frame'] в формате jpg
            status, frame = self.cap.read()
            if not status:
                raise Exception()
            app['frame'] = cv2.imencode('.jpg', frame)[1]
            await asyncio.sleep(1/30)

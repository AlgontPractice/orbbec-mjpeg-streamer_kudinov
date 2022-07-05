import logging
import time
import numpy as np
from aiohttp import web
from aiohttp_cors import CorsViewMixin
from m7_aiohttp.util.logged import logged


logger = logging.getLogger('orbbec-mjpeg-streamer')


class MjpegHandlerService(CorsViewMixin):

    @logged(logger)
    async def mjpeg_handler_rgb(self, request):
        # TODO: реализуем метод, генерирующий mjpeg-поток на основе кадров из переменной app['frame']
        # frame = web.Response(body=np.array(request.app['frame']).tobytes(), content_type='image/jpg')
        # return web.Response(body=frame, content_type='multipart/x-mixed-replace;boundary=--frame', status=200)
        pass
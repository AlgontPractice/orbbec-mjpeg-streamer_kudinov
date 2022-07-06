import logging
import time
import numpy as np
import asyncio
from aiohttp import web
from aiohttp_cors import CorsViewMixin
from m7_aiohttp.util.logged import logged


logger = logging.getLogger('orbbec-mjpeg-streamer')


class MjpegHandlerService(CorsViewMixin):

    @logged(logger)
    async def mjpeg_handler_rgb(self, request):



        # TODO: реализуем метод, генерирующий mjpeg-поток на основе кадров из переменной app['frame']
        while True:    
            frame = web.Response(content_type='image/jpeg', body=np.array(request.app['frame']).tobytes())
            await frame.prepare(request)
            await frame.write(np.array(request.app['frame']).tobytes())
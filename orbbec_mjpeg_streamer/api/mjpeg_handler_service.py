import logging
import time
import numpy as np
import asyncio
import cv2
from aiohttp import web, MultipartWriter
from aiohttp_cors import CorsViewMixin
from m7_aiohttp.util.logged import logged


logger = logging.getLogger('orbbec-mjpeg-streamer')


class MjpegHandlerService(CorsViewMixin):

    @logged(logger)
    async def mjpeg_handler_rgb(self, request):
        # TODO: реализуем метод, генерирующий mjpeg-поток на основе кадров из переменной app['frame']
        my_boundary = 'boundary'
        response = web.StreamResponse(
            status=200,
            reason='OK',
            headers={
                'Content-Type': 'multipart/x-mixed-replace;boundary={}'.format(my_boundary)
            }
        )
        await response.prepare(request)
        while True:
            frame = np.array(request.app['frame']).tobytes()
            with MultipartWriter('image/jpeg', boundary=my_boundary) as mpwriter:
                mpwriter.append(frame, {
                    'Content-Type': 'image/jpeg'
                })
                await mpwriter.write(response, close_boundary=False)
            await response.drain()

    # @logged(logger)
    # async def mjpeg_handler_depth(self, request):
    #     my_boundary = 'boundary'
    #     response = web.StreamResponse(
    #         status=200,
    #         reason='OK',
    #         headers={
    #             'Content-Type': 'multipart/x-mixed-replace;boundary={}'.format(my_boundary)
    #         }
    #     )
    #     await response.prepare(request)
    #     while True:
    #         frame = np.array(request.app['depthmap']).tobytes()
    #         with MultipartWriter('image/jpeg', boundary=my_boundary) as mpwriter:
    #             mpwriter.append(frame, {
    #                 'Content-Type': 'image/jpeg'
    #             })
    #             await mpwriter.write(response, close_boundary=False)
    #         await response.drain()

    # @logged(logger)
    # async def mjpeg_handler_min(self, request):
    #     my_boundary = 'boundary'
    #     response = web.StreamResponse(
    #         status=200,
    #         reason='OK',
    #         headers={
    #             'Content-Type': 'multipart/x-mixed-replace;boundary={}'.format(my_boundary)
    #         }
    #     )
    #     await response.prepare(request)
    #     while True:
    #         img = request.app['minimal']
    #         with MultipartWriter('text/plain', boundary=my_boundary) as mpwriter:
    #             mpwriter.append(str(img), {
    #                 'Content-Type': 'text/plain',
    #                 'Content-length': str(len(str(img)))
    #             })
    #             await mpwriter.write(response, close_boundary=False)
    #         await response.drain()

import asyncio
import cv2
from aiohttp import web
from aiopg.sa import create_engine
import sqlalchemy as sa
from aiohttp_jsonrpc import handler
import time
import numpy as np

class JSONRPCServer(handler.JSONRPCView):
    async def rpc_take_picture(self):
        cv2.samples.addSamplesDataSearchPath('/etc/cam2_kudinov/orbbec-mjpeg-streamer_kudinov/opencv_samples/')
        Cascade = cv2.CascadeClassifier()
        Cascade.load(cv2.samples.findFile('haarcascade_frontalface_alt.xml'))
        if Cascade.empty():
            raise Exception()
            
        is_empty = True
        t_end = time.time() + 10
        while time.time() < t_end:
            frame = cv2.imdecode(self.request.app['frame'], cv2.IMREAD_UNCHANGED)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.equalizeHist(frame_gray)
            recs = Cascade.detectMultiScale(frame_gray)
            for (x, y, w, h) in recs:
                is_empty = not bool(x)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            if not is_empty:
                break

        if is_empty:
            raise Exception('Face not found')

        if not is_empty:
            frame_raw = np.array(cv2.imencode('.jpg', frame)[1]).tobytes()
            tbl = sa.Table('images', sa.MetaData(),
               sa.Column('img', sa.LargeBinary()),
               sa.Column('time', sa.TIMESTAMP()))
            db_frame = None
            async with create_engine(user='postgres', database='idb_kudinov', host='192.168.1.245', port='5432', password='postgres') as engiene:
                async with engiene.acquire() as connection:
                    await connection.execute(tbl.insert().values(img = frame_raw, time=sa.func.now()))
                    
        return 'OK'

    async def rpc_get_list(self):
        tbl = sa.Table('images', sa.MetaData(),
               sa.Column('img', sa.LargeBinary()),
               sa.Column('time', sa.TIMESTAMP()))
        db_num = None
        db_list = []
        async with create_engine(user='postgres', database='idb_kudinov', host='192.168.1.245', port='5432', password='postgres') as engiene:
            async with engiene.acquire() as connection:
                async for row in await connection.execute(sa.select([sa.func.count()]).select_from(tbl)):
                    db_num = row[0]
                async for row in await connection.execute(sa.select([tbl.columns.time])):
                    db_list.append(str(row.time))
        
        
        
        return {'num': db_num, 'list': db_list}
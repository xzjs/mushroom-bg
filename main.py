import asyncio
import base64
from fastapi import FastAPI, Response
import cv2
import concurrent.futures
from model import Size, Signal
import redis

import numpy as np

app = FastAPI()

video_capture = cv2.VideoCapture(6)
process_pool_executor = concurrent.futures.ProcessPoolExecutor()
black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
placeholder = Response(content=base64.b64decode(
    black_1px.encode('ascii')), media_type='image/png')
r = redis.Redis(host='127.0.0.1', port=6379)
keys = ('mushroom2', 'mushroom3', 'mushroom4', 'mushroom5', 'mushroom6')
indexs = [2,3,4,5,6]


def convert(frame: np.ndarray) -> bytes:
    _, imencode_image = cv2.imencode('.jpg', frame)
    return imencode_image.tobytes()


@app.get('/api/camera')
async def grab_video_frame() -> Response:
    if not video_capture.isOpened():
        return placeholder
    loop = asyncio.get_running_loop()
    _, frame = await loop.run_in_executor(None, video_capture.read)
    if frame is None:
        return placeholder
    jpeg = await loop.run_in_executor(process_pool_executor, convert, frame)
    return Response(content=jpeg, media_type='image/jpeg')


@app.post('/api/size')
def size(size: Size):
    r.set('max', size.max)
    r.set('min', size.min)
    return


@app.post('/api/signal')
def signal(signal: Signal):
    if (signal.action == 'start'):
        r.delete(keys)
    r.publish('signal', signal.action)
    return


@app.get('/api/statistics')
def statistics():
    m = r.mget(keys)
    return {'keys': indexs, 'values': m}

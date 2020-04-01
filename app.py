import numpy as np
from PIL import Image
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
from model import text_predict
from redisMQ.redisbase import redisDataBase

# imgString = data['imgString'].encode().split(b';base64,')[-1]

app = Flask(__name__)
redis_mq = redisDataBase()


@app.route("/ocr", methods=["POST"])
def ocr():
    data = request.json()
    ocr_identify(data.get("image_path"))


def ocr_identify(image_path):
    try:
        image = Image.open(image_path)
        if image is not None:
            image = np.array(image)
        return text_predict(image)
    except Exception as e:
        return {"status": "fail", "reason": repr(e)}


ThreadPoolExecutor().submit(redis_mq.listen_task, ocr_identify)
ThreadPoolExecutor().submit(redis_mq._ping)

app.run()

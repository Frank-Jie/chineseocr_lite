import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from model import text_predict
from redisMQ.redisbase import redisDataBase
from config import *

app = Flask(__name__)


# redis_mq = redisDataBase()


@app.route("/ocr", methods=["POST"])
def ocr():
    file = request.files.get("image_body")
    if file == None:
        file = request.json.get("image_path")
    result = ocr_identify(file)
    return jsonify(result), 200


def ocr_identify(image_path):
    try:
        image = Image.open(image_path)
        if image is not None:
            image = np.array(image)
        if image.shape[-1] == 4:
            image = image[:, :, :3]
        return text_predict(image)
    except Exception as e:
        return {"status": "fail", "reason": repr(e)}


# redis订阅-发布模式  用于相同server内  暂时不使用
# executer = ThreadPoolExecutor()
# executer.submit(redis_mq.listen_task, ocr_identify)
# executer.submit(redis_mq._ping)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

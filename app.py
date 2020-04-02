import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from model import text_predict
from redisMQ.redisbase import redisDataBase


app = Flask(__name__)
redis_mq = redisDataBase()

flag = True
@app.route("/ocr", methods=["POST"])
def ocr():
    if flag == False:
        return jsonify({"status":"busy"})
    file = request.files.get("image_body")
    if file == None:
        file = request.json.get("image_path")
    result = ocr_identify(file)
    return jsonify(result)


def ocr_identify(image_path):
    global flag
    try:
        flag = False
        image = Image.open(image_path)
        if image is not None:
            image = np.array(image)
        return text_predict(image)
    except Exception as e:
        return {"status": "fail", "reason": repr(e)}
    finally:
        flag = True



# ThreadPoolExecutor().submit(redis_mq.listen_task, ocr_identify)
# ThreadPoolExecutor().submit(redis_mq._ping)

app.run()

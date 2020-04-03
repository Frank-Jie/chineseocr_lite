import celery
import numpy as np
from PIL import Image
from celery import Celery
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
    task = ocr_identify.apply_async(file)
    return jsonify({"task_id": task.id}), 202


@celery.task()
def ocr_identify(image_path):
    try:
        image = Image.open(image_path)
        if image is not None:
            image = np.array(image)
        return text_predict(image)
    except Exception as e:
        return {"status": "fail", "reason": repr(e)}


@app.route('/ocr_status/<task_id>')
def taskstatus(task_id):
    task = ocr_identify.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'status': 'Pending...',
            'info': str(task.info)
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'info': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


# redis订阅-发布模式  用于相同server内  暂时不使用
# executer = ThreadPoolExecutor()
# executer.submit(redis_mq.listen_task, ocr_identify)
# executer.submit(redis_mq._ping)

app.config['CELERY_BROKER_URL'] = f"redis://:{REDIS_PASSWORD}@{REDIS_IP}:6379/1"
app.config['CELERY_RESULT_BACKEND'] = f"redis://:{REDIS_PASSWORD}@{REDIS_IP}:6379/2"
app.config['CELERY_RESULT_SERIALIZER'] = "json"
app.config['CELERY_TASK_RESULT_EXPIRES'] = 60 * 5
# app.run(host=IP, port=PORT)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

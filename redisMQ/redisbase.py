import base64
import json
import time

import redis
import six
from PIL import Image

from config import *

class redisDataBase:

    def __init__(self):
        self.conn = redis.Redis(
            connection_pool=redis.ConnectionPool.from_url(f"redis://:{REDIS_PASSWORD}@{REDIS_IP}:6379/0",
                                                          decode_responses=True))
        self.job_key = job_list_key_name
        self.result_key = result_key_name
        self.ps = self.conn.pubsub()
        self.ps.subscribe(job_list_key_name)


    def pub_result(self, result, id):
        try:
            result.update({"id": id})
            res = self.conn.publish(result_key_name, json.dumps(result))
        except Exception as e:
            print(e)


    def listen_task(self, callback):
        try:
            for i in self.ps.listen():
                if i['type'] == 'message':
                    data = json.loads(i["data"])
                    id = data.get("id")
                    if flag == False:
                        self.pub_result({"status":"busy"}, id)
                    ocr_result = callback(data.get("path"))
                    self.pub_result(ocr_result, id)
        except Exception as e:
            print(repr(e))


    def _ping(self):
        while True:
            time.sleep(1000)
            if not self.conn.ping():
                print("oops~ redis-server get lost. call him back now!")
                self.conn = redis.Redis(connection_pool=redis.ConnectionPool(host=ip, port=6379, decode_responses=True))
                self.ps = self.conn.pubsub()
                self.ps.subscribe(job_list_key_name)


    @staticmethod
    def base64_to_PIL(string):
        """
        base64 string to PIL
        """
        try:
            base64_data = base64.b64decode(string)
            buf = six.BytesIO()
            buf.write(base64_data)
            buf.seek(0)
            img = Image.open(buf).convert('RGB')
            return img
        except:
            return None

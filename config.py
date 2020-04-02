import os

filt_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(filt_path) + os.path.sep + ".")
offset_w = 3
offset_h = 3
min_pic_size = 400
score_threshold = 0.7
GPU_ID = None

# psenet相关
pse_long_size = 960  # 图片长边
pse_model_type = "mobilenetv2"
pse_scale = 1
pse_model_path = os.path.join(father_path, "models/psenet_lite_mbv2.pth")

# crnn相关
nh = 256
crnn_type = "lite_lstm"
if crnn_type == "lite_lstm":
    LSTMFLAG = True
    crnn_model_path = os.path.join(father_path, "models/crnn_lite_lstm_dw_v2.pth")
elif crnn_type == "lite_dense":
    LSTMFLAG = False
    crnn_model_path = os.path.join(father_path, "models/crnn_lite_dense_dw.pth")
elif crnn_type == "full_lstm":
    LSTMFLAG = True
    crnn_model_path = os.path.join(father_path, "models/ocr-lstm.pth")
elif crnn_type == "full_dense":
    LSTMFLAG = False
    crnn_model_path = os.path.join(father_path, "models/ocr-dense.pth")

job_list_key_name = 'job_list_table'
result_key_name = 'result_set_table'
image_key_name = 'img_string_table'
ip = "localhost"
TIMEOUT = 30

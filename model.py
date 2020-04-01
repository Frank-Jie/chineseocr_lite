import numpy as np
from PIL import Image
from crnn.keys import alphabetChinese as alphabet
from config import *
from crnn import FullCrnn, LiteCrnn, CRNNHandle
from psenet import PSENet, PSENetHandel
from utils import crop_rect

text_detect_net = PSENet(backbone=pse_model_type, pretrained=False, result_num=6, scale=pse_scale)

text_handle = PSENetHandel(pse_model_path, text_detect_net, pse_scale, gpu_id=GPU_ID)
crnn_net = None

if crnn_type == "full_lstm" or crnn_type == "full_dense":
    crnn_net = FullCrnn(32, 1, len(alphabet) + 1, nh, n_rnn=2, leakyRelu=False, lstmFlag=LSTMFLAG)
elif crnn_type == "lite_lstm" or crnn_type == "lite_dense":
    crnn_net = LiteCrnn(32, 1, len(alphabet) + 1, nh, n_rnn=2, leakyRelu=False, lstmFlag=LSTMFLAG)

assert crnn_type is not None
crnn_handle = CRNNHandle(crnn_model_path, crnn_net, gpu_id=GPU_ID)



def crnnRec(im, rects_re):
    """
    crnn模型，ocr识别
    @@model,
    @@converter,
    @@im:Array
    @@text_recs:text box
    @@ifIm:是否输出box对应的img

    """
    results = []
    im = Image.fromarray(im)
    for index, rect in enumerate(rects_re):

        degree, w, h, cx, cy = rect
        partImg = crop_rect(im, ((cx, cy), (h, w), degree))
        partImg = Image.fromarray(partImg).convert("RGB")
        # L = 灰度图像
        partImg_ = partImg.convert('L')
        simPred = crnn_handle.predict(partImg_)  ##识别的文本

        if simPred.strip() != u'':
            results.append({'cx': cx, 'cy': cy, 'text': simPred})
    return results


def text_predict(img):
    preds, boxes_list, rects_re, t = text_handle.predict(img, long_size=pse_long_size)
    result =  crnnRec(np.array(img), rects_re)
    return {"status": "success", "result_list": result}



if __name__ == "__main__":
    pass

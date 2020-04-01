import cv2
import numpy as np


def crop_rect(img, rect, alph=0.15):
    img = np.asarray(img)
    # get the parameter of the small rectangle
    center, size, angle = rect[0], rect[1], rect[2]
    min_size = min(size)
    if (angle > -45):
        center, size = tuple(map(int, center)), tuple(map(int, size))
        size = (int(size[0] + min_size * alph), int(size[1] + min_size * alph))
        height, width = img.shape[0], img.shape[1]
        M = cv2.getRotationMatrix2D(center, angle, 1)
        img_rot = cv2.warpAffine(img, M, (width, height))
        img_crop = cv2.getRectSubPix(img_rot, size, center)
    else:
        center = tuple(map(int, center))
        size = tuple([int(rect[1][1]), int(rect[1][0])])
        size = (int(size[0] + min_size * alph), int(size[1] + min_size * alph))
        angle -= 270
        height, width = img.shape[0], img.shape[1]
        M = cv2.getRotationMatrix2D(center, angle, 1)
        img_rot = cv2.warpAffine(img, M, (width, height))
        img_crop = cv2.getRectSubPix(img_rot, size, center)
    return img_crop

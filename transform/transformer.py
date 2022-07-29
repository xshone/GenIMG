# encoding: utf-8
# @file: transformer
# @author: XiongJie
# @time: 2022/7/28 11:46
import cv2 as cv
import os
import numpy as np
from PIL import Image
from transform.rgb import RGBTransform


class Transformer:
    def __init__(self, image_path: str):
        self.image_path = image_path

    def convert_color(self, r: int, g: int, b: int):
        if not os.path.exists(self.image_path):
            return

        img = cv.imread(self.image_path)
        cv.imshow('Origin', img)
        img_bgr = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        cv.imshow('HSV', img_bgr)
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        cv.imshow('RGB', img_rgb)
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imshow('Gray', img_gray)
        cv.waitKey(0)


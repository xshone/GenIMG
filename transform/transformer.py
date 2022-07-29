# encoding: utf-8
# @file: transformer
# @author: XiongJie
# @time: 2022/7/28 11:46
import os

import cv2 as cv
from PIL import Image

from transform.core import RGBTransform


class Transformer:
    def __init__(self, image_path: str, output_path: str, output_ext: str):
        self.image_path = image_path
        self.output_path = output_path
        self.output_ext = output_ext

    def convert_mode(self, r: int, g: int, b: int):
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

    def convert_color(self, rgb: tuple, factor: float):
        if not os.path.exists(self.image_path):
            return

        img = Image.open(self.image_path)
        img = img.convert('RGBA')
        transformer = RGBTransform()
        red_m = transformer.mix_with(base_color=rgb, factor=factor)
        red = red_m.applied_to(img)
        red.save(self.output_path, self.output_ext)

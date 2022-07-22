# encoding: utf-8
# @file: util
# @author: XiongJie
# @time: 2022/7/20 15:43
import os


def get_file_ext(file_path: str):
    split = os.path.splitext(file_path)

    if split:
        return os.path.splitext(file_path)[1]

    return ''


def is_supported_image_file(file_ext: str):
    type_list = ['.bmp', '.gif', '.jpg', '.jpeg', '.png']

    if file_ext.lower() in type_list:
        return True

    return False

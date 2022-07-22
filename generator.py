import json
import os.path
import time

from PIL import Image, ImageFile

import util


class Layer:
    def __init__(self, image_path: str):
        self.image_path = image_path


class PicItem:
    def __init__(self, pic_id: str, layers: [Layer]):
        self.pic_id = pic_id
        self.layers = layers


class Generator:
    def __init__(self, config_path: str):
        json_str = "{}"

        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                json_str = f.read()

        self.config = json.loads(json_str)
        self.assets_dir = str(self.config.get("assets_dir", ""))
        self.output_dir = str(self.config.get("output_dir", ""))
        self.image_mode = str(self.config.get("image_mode", ""))

        if os.path.exists(self.assets_dir):
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)

    def check_assets(self) -> bool:
        """
        检查组件图层素材
        :return:
        """
        print("### Checking files...")
        for root, dirs, files in os.walk(self.assets_dir):
            for file in files:
                file_ext = util.get_file_ext(file_path=file).lower()

                if not util.is_supported_image_file(file_ext):
                    return False

        return True

    def composite_layers(self, layers: [Layer]) -> ImageFile.ImageFile:
        """
        合成各图层
        :param layers: 图层列表
        :return:
        """
        current_index = 0
        current_composite = Image.open(layers[current_index].image_path).convert(self.image_mode)

        while current_index < len(layers):
            if current_index >= 1:
                new_layer = Image.open(layers[current_index].image_path).convert(self.image_mode)
                current_composite = Image.alpha_composite(current_composite, new_layer)

            current_index += 1

        return current_composite

    def generate(self, pic_items: [PicItem]):
        """
        根据合成图片配置项开始生成合成
        :param pic_items: 合成图片配置项列表
        :return:
        """
        for item in pic_items:
            save_path = os.path.join(self.output_dir, f"{item.pic_id}.png")
            final_composite = self.composite_layers(layers=item.layers)
            final_composite.save(save_path)
            print(f"<<< Saving composite image: {save_path}")

    def select_pic(self, part_configs: dict) -> [PicItem]:
        """
        准备合成图片配置项列表
        :param part_configs: 各部分的配置
        :return:
        """
        pic_item_list = []

        # 按layer_index由低到高整理Part
        part_configs = sorted(part_configs, key=lambda part: part["layer_index"])
        part_files_list = []

        # 获取各部件的文件路径列表
        for part_config in part_configs:
            part_dir = os.path.join(self.assets_dir, part_config["directory"])

            for root, dirs, files in os.walk(part_dir):
                file_paths = []
                for file_name in files:
                    file_paths.append(os.path.join(root, file_name))

                part_files_list.append(file_paths)

        path_index_dict = {}
        part_count = len(part_files_list)
        all_pic_ids = []
        is_part_finished_list = []

        for item in range(len(part_files_list)):
            path_index_dict[item] = 0
            is_part_finished_list.append(False)

        while True:
            is_break = all(is_part_finished_list)

            if is_break:
                break

            layers = []
            id_str_list = []

            for part_index, part_files in enumerate(part_files_list):
                # ----------------------
                #  0  1  0  0  0  1
                # 高位            低位
                # ----------------------
                # 如果当前位part不是最低位，且剩余低位part已经遍历完，则当前位part的index进1
                if part_index != part_count - 1:
                    if all(is_part_finished_list[part_index + 1:]):
                        if path_index_dict[part_index] != len(part_files) - 1:
                            path_index_dict[part_index] += 1

                            lower_part_index = part_index + 1
                            while lower_part_index < part_count:
                                is_part_finished_list[lower_part_index] = False
                                path_index_dict[lower_part_index] = 0
                                lower_part_index += 1

                layer_file_index = path_index_dict[part_index]
                id_str_list.append(str(layer_file_index))
                layers.append(Layer(image_path=part_files[layer_file_index]))

                if path_index_dict[part_index] == len(part_files) - 1:
                    is_part_finished_list[part_index] = True

                # 最低位part不断进位
                if part_index == part_count - 1:
                    if path_index_dict[part_index] != len(part_files) - 1:
                        path_index_dict[part_index] += 1

            pic_id = "_".join(id_str_list)
            print(f">>> Generating [{pic_id}]")

            if pic_id not in all_pic_ids:
                all_pic_ids.append(pic_id)
                new_pic_item = PicItem(pic_id=pic_id, layers=layers)
                self.generate([new_pic_item])
                pic_item_list.append(new_pic_item)

        return pic_item_list

    def run(self):
        start_time = time.time()
        is_checked = self.check_assets()

        if not is_checked:
            print(f"[Error] Not all image files format are supported.")
            return

        part_configs = self.config.get("parts", [])

        if len(part_configs) == 0:
            print(f"[Error] No part config found.")
            return

        # pic_items = self.select_pic(part_configs=part_configs)
        # self.generate(pic_items=pic_items)
        self.select_pic(part_configs=part_configs)

        print(f"*** TIME ELAPSED: {round(time.time() - start_time, 2)} s")
        print(f"[ALL DONE]")

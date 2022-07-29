import json
import os

from gen.generator import Generator
from transform.transformer import Transformer


def gen():
    config_path = "config/gen.json"

    g = Generator(config_path=config_path)
    g.run()


def transform():
    config_path = "config/transform.json"
    json_str = "{}"

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            json_str = f.read()

    config = json.loads(json_str)
    image_path = str(config.get("image_path", ""))
    output_dir = str(config.get("output_dir", ""))
    colors = config.get("colors")

    for color in colors:
        output_path = os.path.join(output_dir, f"{color['name']}.png")
        t = Transformer(image_path=image_path, output_path=output_path, output_ext='PNG')
        t.convert_color(rgb=tuple(color['rgb']), factor=config['factor'])


def main():
    transform()


if __name__ == '__main__':
    main()

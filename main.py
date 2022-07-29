from gen.generator import Generator
from transform.transformer import Transformer


def gen():
    config_path = "./config.json"

    g = Generator(config_path=config_path)
    g.run()


def transform():
    image_path = r"./assets/face/panda.png"
    t = Transformer(image_path=image_path)
    t.convert_color(r=0, g=0, b=0)


def main():
    transform()


if __name__ == '__main__':
    main()

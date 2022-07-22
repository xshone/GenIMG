import os.path

from generator import Generator


def main():
    config_path = "./config.json"

    g = Generator(config_path=config_path)
    g.run()


if __name__ == '__main__':
    main()

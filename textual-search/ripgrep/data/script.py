"""Small utility script used for grep exercises."""

import sys


def load_config(path):
    with open(path) as f:
        return f.read()


def process(data):
    # TODO: gérer le cas d'erreur si le fichier est vide
    return data.strip().splitlines()


def main():
    config = load_config("config.conf")
    lines = process(config)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()

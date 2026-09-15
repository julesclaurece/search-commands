"""Entry point for the demo application."""

from utils import helper


def run():
    # TODO: valider les arguments avant de lancer le traitement
    data = helper()
    print(data)


if __name__ == "__main__":
    run()

"""Point d'entrée de l'application de démo."""

import json


def load_settings():
    # TODO: valider le schéma JSON avant de le charger
    with open("settings.json") as f:
        return json.load(f)


def main():
    settings = load_settings()
    print(settings)


if __name__ == "__main__":
    main()

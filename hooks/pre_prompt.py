import os
import sys


def is_composer_in_path() -> bool:
    from shutil import which

    return which("composer") is not None


def populate_layer_choices():
    import urllib.request
    import json

    contents = urllib.request.urlopen(
        "https://raw.githubusercontent.com/brefphp/bref/master/layers.json"
    )
    layers = json.load(contents)

    cookiecutter_json = os.path.join(os.getcwd(), "cookiecutter.json")

    with open(cookiecutter_json, "r+") as f:
        data = json.load(f)
        f.seek(0)
        data["php_version"] = list(layers.keys())
        data["aws_region"] = list(next(iter(layers.values())).keys())
        data["_bref_layers"] = layers
        json.dump(data, f)


if __name__ == "__main__":
    populate_layer_choices()
    if not is_composer_in_path():
        print("ERROR: Composer is not installed.")
        sys.exit(1)

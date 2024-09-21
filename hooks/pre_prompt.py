import os
import sys


def is_composer_in_path() -> bool:
    from shutil import which

    return which("composer") is not None


def populate_layer_choices(ref):
    import urllib.request
    import json

    contents = urllib.request.urlopen(
        f"https://raw.githubusercontent.com/brefphp/bref/{ref}/layers.json"
    )
    layers = json.load(contents)

    cookiecutter_json = os.path.join(os.getcwd(), "cookiecutter.json")

    with open(cookiecutter_json, "r+") as f:
        data = json.load(f)
        f.seek(0)
        data["aws_region"] = list(next(iter(layers.values())).keys())
        data["_bref_layers"] = layers
        json.dump(data, f)


if __name__ == "__main__":
    populate_layer_choices("refs/tags/2.3.5")
    if not is_composer_in_path():
        print("ERROR: Composer is not installed.")
        sys.exit(1)

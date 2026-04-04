import os
import sys
import urllib.request
import json
from shutil import which
from typing import Dict, Any, TextIO


def _composer_is_installed() -> bool:
    """
    Check if Composer is installed.

    :return:
    """
    return which("composer") is not None


def _get_aws_regions(layers: Dict[str, Any]) -> list:
    """
    Get the available AWS regions from the Bref layers.

    :param layers:
    :return:
    """
    return list(next(iter(layers.values())).keys())


def populate_layer_choices(ref: str) -> None:
    """
    Populate the cookiecutter.json file with the available AWS regions and Bref layers.

    :param ref: Git reference to fetch the layers from.
    :return: None
    """
    layer_url = f"https://raw.githubusercontent.com/brefphp/bref/{ref}/layers.json"
    with urllib.request.urlopen(layer_url) as response:  # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
        layers = json.load(response)

    cookiecutter_json_path = os.path.join(os.getcwd(), "cookiecutter.json")

    fp: TextIO
    with open(cookiecutter_json_path, "r+") as fp:
        data = json.load(fp)
        fp.seek(0)
        data["aws_region"] = _get_aws_regions(layers)
        data["_bref_layers"] = layers
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    populate_layer_choices("refs/tags/3.0.1")
    if not _composer_is_installed():
        print("ERROR: Composer is not installed.")
        sys.exit(1)

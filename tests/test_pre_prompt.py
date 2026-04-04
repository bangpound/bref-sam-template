import io
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))

from pre_prompt import _composer_is_installed, _get_aws_regions, populate_layer_choices

SAMPLE_LAYERS = {
    "arm-php-85-fpm": {"us-east-1": 1, "eu-west-1": 2},
    "php-85": {"us-east-1": 3, "eu-west-1": 4},
}


class TestGetAwsRegions(unittest.TestCase):
    def test_extracts_regions_from_first_layer(self):
        regions = _get_aws_regions(SAMPLE_LAYERS)
        self.assertEqual(regions, ["us-east-1", "eu-west-1"])


class TestComposerIsInstalled(unittest.TestCase):
    def test_returns_true_when_found(self):
        with patch("pre_prompt.which", return_value="/usr/local/bin/composer"):
            self.assertTrue(_composer_is_installed())

    def test_returns_false_when_missing(self):
        with patch("pre_prompt.which", return_value=None):
            self.assertFalse(_composer_is_installed())


class TestPopulateLayerChoices(unittest.TestCase):
    def test_writes_regions_and_layers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cc_json = os.path.join(tmpdir, "cookiecutter.json")
            with open(cc_json, "w") as f:
                json.dump({"aws_region": "", "_bref_layers": {}}, f)

            mock_response = io.BytesIO(json.dumps(SAMPLE_LAYERS).encode())

            with patch("urllib.request.urlopen", return_value=mock_response), \
                 patch("pre_prompt.os.getcwd", return_value=tmpdir):
                populate_layer_choices("refs/tags/2.4.1")

            with open(cc_json) as f:
                data = json.load(f)

        self.assertEqual(data["aws_region"], ["us-east-1", "eu-west-1"])
        self.assertEqual(data["_bref_layers"], SAMPLE_LAYERS)


if __name__ == "__main__":
    unittest.main()

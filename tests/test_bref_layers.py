import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jinja2 import Environment
from extensions.bref_layers import BrefLayersExtension


def _make_env():
    env = Environment(extensions=[BrefLayersExtension])  # nosemgrep: python.flask.security.xss.audit.direct-use-of-jinja2.direct-use-of-jinja2
    return env


class TestBrefPhpLayerName(unittest.TestCase):
    def setUp(self):
        self.env = _make_env()
        self.fn = self.env.globals["bref_php_layer_name"]

    def test_arm64_with_fpm_suffix(self):
        self.assertEqual(self.fn(["arm64"], "85", "fpm"), "arm-php-85-fpm")

    def test_arm64_no_suffix(self):
        self.assertEqual(self.fn(["arm64"], "85"), "arm-php-85")

    def test_x86_64_with_fpm_suffix(self):
        self.assertEqual(self.fn(["x86_64"], "85", "fpm"), "php-85-fpm")

    def test_x86_64_no_suffix(self):
        self.assertEqual(self.fn(["x86_64"], "84"), "php-84")

    def test_console_suffix(self):
        self.assertEqual(self.fn(["arm64"], "85", "console"), "arm-php-85-console")


class TestBrefLayerVersion(unittest.TestCase):
    def setUp(self):
        self.env = _make_env()
        self.fn = self.env.globals["bref_layer_version"]

    def test_looks_up_version(self):
        layers = {"arm-php-85-fpm": {"us-east-1": 42, "eu-west-1": 7}}
        self.assertEqual(self.fn(layers, "arm-php-85-fpm", "us-east-1"), 42)
        self.assertEqual(self.fn(layers, "arm-php-85-fpm", "eu-west-1"), 7)

    def test_raises_on_missing_layer(self):
        with self.assertRaises(KeyError):
            self.fn({}, "arm-php-85-fpm", "us-east-1")

    def test_raises_on_missing_region(self):
        layers = {"arm-php-85-fpm": {"us-east-1": 1}}
        with self.assertRaises(KeyError):
            self.fn(layers, "arm-php-85-fpm", "ap-southeast-1")


if __name__ == "__main__":
    unittest.main()

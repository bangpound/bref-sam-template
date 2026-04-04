import os
import sys
import tempfile
import unittest

import yaml


class _CfnLoader(yaml.SafeLoader):
    """SafeLoader extended to ignore CloudFormation intrinsic function tags."""


_CfnLoader.add_multi_constructor("!", lambda loader, tag_suffix, node: node.value)


def _cfn_yaml_load(content):
    return yaml.load(content, Loader=_CfnLoader)  # noqa: S506


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from cookiecutter.generate import generate_files

BREF_LAYERS = {
    "arm-php-85-fpm": {"us-east-1": 11},
    "arm-php-85": {"us-east-1": 22},
    "console": {"us-east-1": 33},
    "php-85-fpm": {"us-east-1": 44},
    "php-85": {"us-east-1": 55},
}

BASE_CONTEXT = {
    "project_name": "Test Project",
    "project_slug": "test_project",
    "runtime": "provided.al2023",
    "architectures": {"value": ["arm64"]},
    "php_version": "85",
    "aws_region": "us-east-1",
    "_bref_layers": BREF_LAYERS,
    "_extensions": ["extensions.bref_layers.BrefLayersExtension"],
}


def _render(extra=None):
    ctx = {**BASE_CONTEXT, **(extra or {})}
    with tempfile.TemporaryDirectory() as tmpdir:
        generate_files(
            repo_dir=PROJECT_ROOT,
            context={"cookiecutter": ctx},
            output_dir=tmpdir,
            overwrite_if_exists=True,
            accept_hooks=False,
        )
        template_yaml = os.path.join(tmpdir, ctx["project_slug"], "template.yaml")
        with open(template_yaml) as f:
            return f.read()


class TestTemplateRenders(unittest.TestCase):
    def test_renders_without_error(self):
        content = _render()
        self.assertIn("HelloWorldFunction", content)
        self.assertIn("ConsoleFunction", content)

    def test_template_yaml_is_valid_yaml(self):
        doc = _cfn_yaml_load(_render())
        self.assertIn("Resources", doc)
        self.assertIn("HelloWorldFunction", doc["Resources"])
        self.assertIn("ConsoleFunction", doc["Resources"])

    def test_arm64_uses_arm_prefix_in_layer_names(self):
        content = _render({"architectures": {"value": ["arm64"]}})
        self.assertIn("arm-php-85-fpm", content)
        self.assertIn("arm-php-85", content)

    def test_x86_64_omits_arm_prefix(self):
        content = _render({"architectures": {"value": ["x86_64"]}})
        self.assertNotIn("arm-php", content)
        self.assertIn("php-85-fpm", content)

    def test_layer_arns_contain_correct_versions(self):
        content = _render()
        self.assertIn(":11", content)  # FPM layer
        self.assertIn(":22", content)  # PHP layer
        self.assertIn(":33", content)  # Console layer

    def test_architecture_appears_in_output(self):
        content = _render()
        self.assertIn("arm64", content)

    def test_project_name_in_description(self):
        content = _render({"project_name": "My Test App", "project_slug": "my_test_app"})
        self.assertIn("My Test App", content)

    def test_aws_region_in_layer_arns(self):
        content = _render({"aws_region": "us-east-1"})
        self.assertIn("us-east-1", content)

    def test_runtime_in_output(self):
        doc = _cfn_yaml_load(_render())
        hello = doc["Resources"]["HelloWorldFunction"]["Properties"]
        self.assertEqual(hello["Runtime"], "provided.al2023")

    def test_console_function_timeout(self):
        doc = _cfn_yaml_load(_render())
        console = doc["Resources"]["ConsoleFunction"]["Properties"]
        self.assertEqual(console["Timeout"], 900)


if __name__ == "__main__":
    unittest.main()

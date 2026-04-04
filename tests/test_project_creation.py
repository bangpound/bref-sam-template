import os
import stat
import sys
import tempfile
import unittest

import yaml

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

CONTEXT = {
    "project_name": "My SAM Project",
    "project_slug": "my_sam_project",
    "runtime": "provided.al2023",
    "architectures": {"value": ["arm64"]},
    "php_version": "85",
    "aws_region": "us-east-1",
    "_bref_layers": BREF_LAYERS,
    "_extensions": ["extensions.bref_layers.BrefLayersExtension"],
}


class TestProjectCreation(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        generate_files(
            repo_dir=PROJECT_ROOT,
            context={"cookiecutter": CONTEXT},
            output_dir=self.tmpdir,
            overwrite_if_exists=True,
            accept_hooks=False,
        )
        self.project = os.path.join(self.tmpdir, CONTEXT["project_slug"])

    def _path(self, *parts):
        return os.path.join(self.project, *parts)

    # --- File presence ---

    def test_template_yaml_exists(self):
        self.assertTrue(os.path.isfile(self._path("template.yaml")))

    def test_makefile_exists(self):
        self.assertTrue(os.path.isfile(self._path("Makefile")))

    def test_composer_json_exists(self):
        self.assertTrue(os.path.isfile(self._path("composer.json")))

    def test_readme_exists(self):
        self.assertTrue(os.path.isfile(self._path("README.md")))

    def test_remote_console_exists(self):
        self.assertTrue(os.path.isfile(self._path("bin", "remote-console")))

    def test_remote_console_is_executable(self):
        path = self._path("bin", "remote-console")
        mode = os.stat(path).st_mode
        self.assertTrue(mode & stat.S_IXUSR, "bin/remote-console is not executable")

    # --- template.yaml structure ---

    def test_template_yaml_has_hello_world_function(self):
        with open(self._path("template.yaml")) as f:
            doc = _cfn_load(f.read())
        self.assertIn("HelloWorldFunction", doc["Resources"])

    def test_template_yaml_has_console_function(self):
        with open(self._path("template.yaml")) as f:
            doc = _cfn_load(f.read())
        self.assertIn("ConsoleFunction", doc["Resources"])

    def test_hello_world_has_api_event(self):
        with open(self._path("template.yaml")) as f:
            doc = _cfn_load(f.read())
        events = doc["Resources"]["HelloWorldFunction"]["Properties"]["Events"]
        self.assertIn("HelloWorld", events)

    def test_console_function_timeout_is_900(self):
        with open(self._path("template.yaml")) as f:
            doc = _cfn_load(f.read())
        timeout = doc["Resources"]["ConsoleFunction"]["Properties"]["Timeout"]
        self.assertEqual(timeout, 900)

    def test_both_functions_use_makefile_build(self):
        with open(self._path("template.yaml")) as f:
            doc = _cfn_load(f.read())
        for fn in ("HelloWorldFunction", "ConsoleFunction"):
            method = doc["Resources"][fn]["Metadata"]["BuildMethod"]
            self.assertEqual(method, "makefile", f"{fn} BuildMethod is not makefile")

    # --- .gitignore ---

    def test_gitignore_exists(self):
        self.assertTrue(os.path.isfile(self._path(".gitignore")))

    def test_gitignore_excludes_vendor(self):
        with open(self._path(".gitignore")) as f:
            content = f.read()
        self.assertIn("vendor/", content)

    def test_gitignore_excludes_sam_build_dir(self):
        with open(self._path(".gitignore")) as f:
            content = f.read()
        self.assertIn(".aws-sam/", content)

    # --- Makefile ---

    def test_makefile_has_build_targets(self):
        with open(self._path("Makefile")) as f:
            content = f.read()
        self.assertIn("build-HelloWorldFunction", content)
        self.assertIn("build-ConsoleFunction", content)


class _CfnLoader(yaml.SafeLoader):
    pass


_CfnLoader.add_multi_constructor("!", lambda loader, tag_suffix, node: node.value)


def _cfn_load(content):
    return yaml.load(content, Loader=_CfnLoader)  # noqa: S506


if __name__ == "__main__":
    unittest.main()

"""Jinja2 extensions."""

import json

from jinja2.ext import Extension


class BrefLayersExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def bref_php_layer_name(archs, php_version, suffix=None):
            cpu_prefix = "arm-" if archs[0] == "arm64" else ""
            name_suffix = f"{'-' + suffix if suffix is not None else ''}"
            return f"{cpu_prefix}php-{php_version}{name_suffix}"

        def bref_layer_version(layers, layer_name, aws_region):
            return layers[layer_name][aws_region]

        environment.globals.update(bref_php_layer_name=bref_php_layer_name)
        environment.globals.update(bref_layer_version=bref_layer_version)

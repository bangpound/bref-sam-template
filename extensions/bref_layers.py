"""Jinja2 extensions."""

import json

from jinja2.ext import Extension


class BrefLayersExtension(Extension):
    """Jinja2 extension to convert a Python object to JSON."""

    def __init__(self, environment):
        """Initialize the extension with the given environment."""
        super().__init__(environment)

        def bref_php_layer_name(archs, php_version, variant=None):
            return f"{'arm-' if archs[0] == 'arm64' else ''}php-{php_version}{'-fpm' if variant == 'fpm' else ''}"

        def bref_layer_version(layers, layer_name, aws_region):
            return layers[layer_name][aws_region]

        environment.globals.update(bref_php_layer_name=bref_php_layer_name)
        environment.globals.update(bref_layer_version=bref_layer_version)

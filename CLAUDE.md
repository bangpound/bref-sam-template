# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template that generates a Symfony 7.3 application configured to run on AWS Lambda using [Bref](https://bref.sh/) and [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) instead of the Serverless Framework.

## Template Usage

```bash
sam init --location gh:bangpound/bref-sam-template --output-dir project --name sam-bref-demo --architecture arm64
cd project/sam-bref-demo
sam build
sam deploy
```

## Repository Structure

- `cookiecutter.json` — Template variables: `project_name`, `project_slug`, `runtime`, `architectures`, `php_version`, `aws_region`. The `_bref_layers` and `_extensions` fields are populated/used at generation time.
- `{{ cookiecutter.project_slug }}/` — The generated project template. Jinja2 syntax is used throughout these files.
- `extensions/bref_layers.py` — Custom Jinja2 extension providing two template functions:
  - `bref_php_layer_name(archs, php_version, suffix=None)` — builds the Bref layer name (e.g., `arm-php-85-fpm`)
  - `bref_layer_version(layers, layer_name, aws_region)` — looks up the layer version from the fetched layers data
- `hooks/pre_prompt.py` — Fetches `layers.json` from the Bref GitHub repo and populates `cookiecutter.json` with available AWS regions and layer ARN data. Also validates that Composer is installed.
- `hooks/post_gen_project.py` — Runs `composer create-project` in the generated project directory.

## Generated Project Architecture

The generated Symfony project (`{{ cookiecutter.project_slug }}/`) contains:

- `template.yaml` — SAM template defining two Lambda functions:
  - `HelloWorldFunction` — HTTP handler using `php-fpm` Bref layer, triggered via API Gateway at `/hello`
  - `ConsoleFunction` — Symfony console runner using `php` + `console` Bref layers, timeout 900s
- `Makefile` — SAM build targets. `build-ConsoleFunction` and `build-HelloWorldFunction` both call `protobuild`, which copies app files to `$ARTIFACTS_DIR`, runs `composer install --classmap-authoritative --no-dev`, and warms the Symfony cache for prod.
- `bin/remote-console` — Bash script that invokes `ConsoleFunction` remotely via `sam remote invoke`, passing CLI args as a JSON event and pretty-printing the output.
- `composer.json` — Uses `symfony/skeleton` with `flex-require` to install `bref/bref`, `bref/symfony-bridge`, and core Symfony components. Targets Symfony 7.3.

## Key Design Points

- Both Lambda functions use `BuildMethod: makefile`, so `sam build` delegates to the `Makefile` targets rather than using a built-in runtime builder.
- The PHP and FPM layer ARNs are rendered as SAM `Parameters` with defaults computed at template generation time (not hardcoded). This allows overriding at deploy time.
- The `_bref_layers` field in `cookiecutter.json` is empty by default — `hooks/pre_prompt.py` fetches and injects the real data from the Bref repo before the template is rendered.
- `composer.json` is listed in `_copy_without_render` (note: the key has a backtick typo — `_copy_without_render\`` ) to prevent Jinja2 from processing its contents.

## Running Tests

Always use `uv` to run tests — never use `python` or `pip` directly:

```bash
uv run python -m unittest discover -s tests -v
```

Install dev dependencies:
```bash
uv sync --group dev
```

## Updating the Bref Version

The Bref tag is hardcoded in `hooks/pre_prompt.py`:
```python
populate_layer_choices("refs/tags/3.0.1")
```
Update this tag when upgrading to a new Bref release.

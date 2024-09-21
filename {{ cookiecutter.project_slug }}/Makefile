.PHONY: protobuild build-HelloWorldFunction

all: build deploy

build:
	sam build

validate: build
	sam validate

deploy: build validate
	sam deploy --no-confirm-changeset

## These targets are invoked by `sam build` itself, so they do not need to be invoked directly.

artifact:
	mkdir -p php/conf.d
	echo "extension=intl" > php/conf.d/php.ini
	rm .env
	echo "<?php return [];" > .env.local.php
	bin/console cache:clear --env=prod
	bin/console cache:warmup --env=prod

protobuild:
	cp -R .env bin config Makefile public src composer.json composer.lock $(ARTIFACTS_DIR)
	composer install --classmap-authoritative --no-dev --no-scripts --working-dir=$(ARTIFACTS_DIR)
	pushd $(ARTIFACTS_DIR) && $(MAKE) artifact && popd && rm -rf $(ARTIFACTS_DIR)/Makefile

build-ConsoleFunction: protobuild

build-HelloWorldFunction: protobuild

.PHONY: protobuild build-HelloWorldFunction

## These targets are invoked by `sam build` itself, so they do not need to be invoked directly.

protobuild:
	cp -R .env bin config public src composer.json composer.lock $(ARTIFACTS_DIR)
	composer install --classmap-authoritative --no-dev --no-scripts --working-dir=$(ARTIFACTS_DIR)
	pushd $(ARTIFACTS_DIR) && \
mkdir -p php/conf.d && \
echo "extension=intl" > php/conf.d/php.ini && \
rm .env && \
echo "<?php return [];" > .env.local.php && \
bin/console cache:clear --env=prod && \
bin/console cache:warmup --env=prod && \
popd

build-ConsoleFunction: protobuild

build-HelloWorldFunction: protobuild

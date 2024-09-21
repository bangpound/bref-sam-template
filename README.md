Bref template for SAM CLI
=========================

[Bref][] depends on the serverless framework, but this template uses the [AWS SAM CLI][] instead.

[Bref]: https://bref.sh
[AWS SAM CLI]: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

Usage
-----

```bash
sam init --location gh:bangpound/bref-sam-template --output-dir project --name sam-bref-demo --architecture arm64
cd project/sam-bref-demo
sam build
sam deploy
```

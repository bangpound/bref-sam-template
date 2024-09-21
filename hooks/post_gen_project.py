import sys
import subprocess
import logging

logger = logging.getLogger(__name__)


def run_composer_install() -> bool:
    try:
        proc = subprocess.run(
            ["composer", "create-project", "--no-interaction"],
            capture_output=True,
            check=True,
        )
        print(proc.stderr.decode(), end="", file=sys.stderr)
        print(proc.stdout.decode(), end="")
        return True
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode(), end="", file=sys.stderr)
        print(e.stdout.decode(), end="")
    return False


if __name__ == "__main__":
    if not run_composer_install():
        print("ERROR: Composer failed.")
        sys.exit(1)

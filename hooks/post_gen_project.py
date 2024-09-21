import sys
import subprocess

COMPOSER_COMMAND = ["composer", "create-project", "--no-interaction"]


def check_process_status(proc: subprocess.Popen) -> bool:
    retcode = proc.poll()
    if retcode is not None:
        return retcode == 0


def run_composer_create_project() -> bool:
    with subprocess.Popen(
        COMPOSER_COMMAND,
        stdout=sys.stdout,
        stderr=sys.stderr,
    ) as proc:
        while check_process_status(proc) is None:
            pass
        return check_process_status(proc)


if __name__ == "__main__":
    if not run_composer_create_project():
        print("ERROR: Composer failed.")
        sys.exit(1)

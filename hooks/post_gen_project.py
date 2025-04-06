import sys
import subprocess

COMPOSER_COMMAND = ["composer", "create-project", "--no-interaction"]


def _is_process_successful(proc: subprocess.Popen) -> bool:
    """
    Check if the process was successful.
    :param proc: A Popen object representing the process.
    :return: True if the process was successful, False otherwise.
    """
    return proc.poll() == 0


def _create_subprocess(command: list) -> subprocess.Popen:
    """
    Create a subprocess.

    :param command: List of command strings to be executed in the subprocess.
    :return: A Popen object representing the subprocess.
    """
    return subprocess.Popen(command, stdout=sys.stdout, stderr=sys.stderr)


def run_composer_create_project() -> bool:
    """
    Run the composer create-project command.
    :return: True if the process was successful, False otherwise.
    """
    with _create_subprocess(COMPOSER_COMMAND) as proc:
        while proc.poll() is None:
            pass

        return _is_process_successful(proc)


if __name__ == "__main__":
    if not run_composer_create_project():
        print("ERROR: Composer failed.")
        sys.exit(1)

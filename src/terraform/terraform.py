import subprocess
from pathlib import Path

from loguru import logger


def terraform_run():
    work_dir = Path("./src/terraform")
    try:
        ret = subprocess.run(
            ["terraform", "init"],
            cwd=work_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        if ret.stdout:
            logger.info(ret.stdout)
        if ret.stderr:
            logger.error(ret.stderr)

        ret = subprocess.run(
            ["terraform", "plan"],
            cwd=work_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        if ret.stdout:
            logger.info(ret.stdout)
        if ret.stderr:
            logger.error(ret.stderr)
        ret = subprocess.run(
            ["terraform", "apply", "-auto-approve"],
            cwd=work_dir,
            check=True,
            capture_output=True,
            text=True,
        )
        if ret.stdout:
            logger.info(ret.stdout)
        if ret.stderr:
            logger.error(ret.stderr)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running terraform: {e}")


if __name__ == "__main__":
    terraform_run()

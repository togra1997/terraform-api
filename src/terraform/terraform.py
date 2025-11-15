import subprocess
from pathlib import Path


def terraform_run():
    work_dir = Path("./src/terraform")
    try:
        subprocess.run(
            ["terraform", "init"],
            cwd=work_dir,
            check=True,
        )
        subprocess.run(
            ["terraform", "plan"],
            cwd=work_dir,
            check=True,
        )
        subprocess.run(
            ["terraform", "apply", "-auto-approve"],
            cwd=work_dir,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running terraform: {e}")


if __name__ == "__main__":
    terraform_run()

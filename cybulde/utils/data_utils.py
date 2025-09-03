from pathlib import Path
from subprocess import CalledProcessError

from cybulde.utils.utils import get_logger, run_shell_command

Data_UTLIS_LOGGER = get_logger(Path(__file__).name)


def is_dvc_initialized() -> bool:
    dvc_folder = Path.cwd() / ".dvc"
    if dvc_folder.exists():
        return True
    try:
        run_shell_command("dvc root")
        return True
    except Exception:
        return False


def is_git_initialized() -> bool:
    return (Path.cwd() / ".git").exists()


def initialize_dvc() -> None:
    if is_dvc_initialized():
        Data_UTLIS_LOGGER.info("DVC is already initialized")
        return
    Data_UTLIS_LOGGER.info("Initializing DVC")
    run_shell_command("dvc init")
    run_shell_command("dvc config core.analytics false")
    run_shell_command("dvc config core.autostage true")
    run_shell_command("git add .dvc")
    run_shell_command("git commit -m 'Initialized DVC'")


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:
    if not run_shell_command("dvc remote list"):
        Data_UTLIS_LOGGER.info("Initializing DVC storage...")
        run_shell_command(f"dvc remote add -d {dvc_remote_name} {dvc_remote_url}")
        run_shell_command("git add .dvc/config")
        run_shell_command(f"git commit -nm 'Configured remote storage at {dvc_remote_url}' || echo 'Nothing to commit'")
    else:
        Data_UTLIS_LOGGER.info("DVC storage was already initialized...")


def commit_to_dvc(dvc_row_data_folder: str, dvc_remote_name: str) -> None:
    current_version = run_shell_command(
        "git tag --list | grep '^v[0-9]*$' | sed 's/v//' | sort -n | tail -1 || echo '0'"
    ).strip()
    if not current_version:
        current_version = "0"
    next_version = f"v{int(current_version)+1}"

    run_shell_command(f"dvc add {dvc_row_data_folder} || echo 'Already tracked or failed'")
    run_shell_command("git add .")
    run_shell_command(
        f"git commit -m 'Updated version of the data from v{current_version} to {next_version}' || echo 'Nothing to commit'"
    )
    run_shell_command(f"git tag -a {next_version} -m 'Data version {next_version}' || echo 'Tag already exists'")
    run_shell_command(f"dvc push --remote {dvc_remote_name}")
    run_shell_command("git push --follow-tags || echo 'Git push failed - check remote/auth'")
    run_shell_command("git push -f --tags || echo 'Git push tags failed - check remote/auth'")


def make_new_data_version(dvc_row_data_folder: str, dvc_remote_name: str) -> None:
    status: str = run_shell_command(f"dvc status {dvc_row_data_folder}.dvc || echo 'status_check_failed'").strip()
    if "up to date" in status.lower() or not status:
        Data_UTLIS_LOGGER.info("Data and pipelines are up to date.")
        return
    commit_to_dvc(dvc_row_data_folder, dvc_remote_name)

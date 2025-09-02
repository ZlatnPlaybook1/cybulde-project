from pathlib import Path
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
        # Safely commit: continue even if nothing to commit
        run_shell_command(
            f"git commit -nm 'Configured remote storage at {dvc_remote_url}' || echo 'Nothing to commit'"
        )
    else:
        Data_UTLIS_LOGGER.info("DVC storage was already initialized...")


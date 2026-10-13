from pathlib import Path


def get_project_root() -> Path:
    current_path = Path(__file__).resolve()

    markers = {".env", ".github"}

    for parent in current_path.parents:
        if any((parent / marker).exists() for marker in markers):
            return parent
    return current_path.parent

ROOT_DIR = get_project_root()

ENV_PATH = ROOT_DIR / ".env"

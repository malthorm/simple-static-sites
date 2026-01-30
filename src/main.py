from pathlib import Path
from utils import copy_static


def main() -> None:
    project_root = Path(__file__).parent.parent
    static_dir = str(project_root / "static")
    public_dir = str(project_root / "public")

    copy_static(static_dir, public_dir)


if __name__ == "__main__":
    main()

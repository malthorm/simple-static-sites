import logging
import os
import shutil

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def copy_static(src: str, dest: str) -> None:
    if not os.path.exists(src):
        raise FileNotFoundError(f"{src} does not exist")
    if not os.path.isdir(src):
        raise NotADirectoryError(f"{src} is not a directory")

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    _copy_dir_recursive(src, dest)


def _copy_dir_recursive(src_dir: str, dest_dir: str) -> None:
    for name in os.listdir(src_dir):
        src_path = os.path.join(src_dir, name)
        dest_path = os.path.join(dest_dir, name)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            logger.info("copied: %s -> %s", src_path, dest_path)
        else:
            os.mkdir(dest_path)
            _copy_dir_recursive(src_path, dest_path)

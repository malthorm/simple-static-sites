import logging

from os import path, listdir, mkdir
from shutil import copy, rmtree


def make_clean_public() -> None:
    public_path = path.abspath("./public/")
    print(public_path)
    if path.exists(public_path):
        rmtree(public_path)
    mkdir(public_path)


def copy_content(src: str, dst: str) -> None:
    for file in listdir(src):
        print(file)
        if path.exists(file) and path.isfile(file):
            copy(file, dst)
        elif path.exists(file):
            copy_content(file, dst)

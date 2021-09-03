from __future__ import absolute_import, unicode_literals

import logging
import os
import zipfile

from ..info import IS_WIN, ROOT
from .six import ensure_text


def read(full_path):
    sub_file = _get_path_within_zip(full_path)
    with zipfile.ZipFile(ROOT, "r") as zip_file:
        with zip_file.open(sub_file) as file_handler:
            return file_handler.read().decode("utf-8")


def extract(full_path, dest):
    logging.debug("extract %s to %s", full_path, dest)
    sub_file = _get_path_within_zip(full_path)
    with zipfile.ZipFile(ROOT, "r") as zip_file:
        info = zip_file.getinfo(sub_file)
        info.filename = dest.name
        zip_file.extract(info, ensure_text(str(dest.parent)))


def _get_path_within_zip(full_path):
    full_path = os.path.abspath(str(full_path))
    sub_file = full_path[len(ROOT) + 1 :]
    if IS_WIN:
        # paths are always UNIX separators, even on Windows, though __file__ still follows platform default
        sub_file = sub_file.replace(os.sep, "/")
    return sub_file

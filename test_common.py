import pathlib
import pytest
import os

import common


def _read_file(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def test_atomic_write(tmp_path: pathlib.Path) -> None:

    user = os.geteuid()
    group = os.getegid()

    filename = str(tmp_path / "file1")
    with common.atomic_write(filename) as f:
        f.write("hello1")
    assert _read_file(filename) == "hello1"

    filename = str(tmp_path / "file2")
    with common.atomic_write(filename, mode=0o000) as f:
        f.write("hello2")
    assert os.path.exists(filename)
    with pytest.raises(PermissionError):
        # We took away permissions to read the file.
        open(filename)

    filename = str(tmp_path / "file3")
    with common.atomic_write(filename, owner=user, group=group, mode=0o644) as f:
        f.write("hello3")
    assert _read_file(filename) == "hello3"

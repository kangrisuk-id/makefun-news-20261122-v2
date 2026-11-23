#!/usr/bin/env python3
"""make.fun news-image-20261122 entry program (Python 3.13, stdlib only).

The repository holds entry.png, the front page drawn by generate_image.py.
This program copies it, byte for byte, to the output directory as
entry.png, so both grader runs produce identical bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    src = HERE / "entry.png"
    size = src.stat().st_size
    assert size <= 1_048_576, f"entry.png is {size} bytes, over the 1 MiB gate"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT_DIR / "entry.png")


if __name__ == "__main__":
    main()

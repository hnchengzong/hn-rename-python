import argparse
import random
from pathlib import Path
from natsort import natsorted

SORT_TABLE = {
    "natural": lambda f: natsorted(f, key=lambda p: p.name),
    "name": lambda f: sorted(f, key=lambda p: p.name),
    "size": lambda f: sorted(f, key=lambda p: p.stat().st_size),
    "mtime": lambda f: sorted(f, key=lambda p: p.stat().st_mtime),
    "ctime": lambda f: sorted(f, key=lambda p: p.stat().st_ctime),
    "owner": lambda f: sorted(f, key=lambda p: p.stat().st_uid),
    "group": lambda f: sorted(f, key=lambda p: p.stat().st_gid),
    "suffix": lambda f: sorted(f, key=lambda p: p.suffix.lower()),
    "random": lambda f: random.sample(f, len(f)),
}

SORT_CHOICES = list(SORT_TABLE.keys())

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("directory", nargs="?", default=".")
    p.add_argument("-p", "--preview", action="store_true")
    p.add_argument("-y", "--yes", action="store_true")
    p.add_argument("-r", "--recursive", action="store_true")
    p.add_argument("-t", "--time", action="store_true")
    p.add_argument("-s", "--str", type=str)
    p.add_argument("-d", "--dir", action="store_true")
    p.add_argument("-v", "--version", action="version", version="hn-rename v0.2.0")
    p.add_argument("--sort", default="natural", choices=SORT_CHOICES)
    return p.parse_args()

def valid_dir(path: Path):
    absolute_dir = Path(path).expanduser().resolve()
    if not absolute_dir.is_dir():
        print(f"Error: Directory not found - {absolute_dir}")
        exit(1)
    return absolute_dir
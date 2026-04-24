#!/usr/bin/env python3
import argparse
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterator

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

def valid_dir(path : Path):
    absolute_dir = Path(path).expanduser().resolve()
    if not absolute_dir.is_dir():
        print(f"Error: Directory not found - {absolute_dir}")
        sys.exit(1)
    return absolute_dir

def list_items(root : Path, recursive : bool, dir_only : bool):
    items: list[Path] = []
    walker:Iterator[Path] = root.rglob("*") if recursive else root.iterdir()
    for item in walker:
        if item.name.startswith("."):
            continue
        if dir_only and item.is_dir():
            items.append(item)
        if not dir_only and item.is_file():
            items.append(item)
    return items

def sort_items(items:list[Path], mode:str):
    return SORT_TABLE[mode](items)

def make_prefix(args:argparse.Namespace):
    parts:list[str] = []
    if args.time:
        parts.append(datetime.now().strftime("%Y%m%d"))
    if args.str and args.str.strip():
        parts.append(args.str.strip())
    return "_".join(parts) + "_" if parts else ""

def rename_plan(items:list[Path], prefix:str):
    tasks:list[tuple[Path, Path]] = []
    used = set()
    for idx, item in enumerate(items, 1):
        num:str = str(idx)
        suffix:str = item.suffix if item.is_file() else ""
        new_name:str = f"{prefix}{num}{suffix}"
        new_path:Path = item.parent / new_name
        if new_path.exists() or new_name in used:
            print(f"Skipped: {item.name} -> {new_name}")
            continue
        tasks.append((item, new_path))
        used.add(new_name)
    return tasks

def show(all_tasks, preview):
    show_title = "Preview" if preview else "Pending"
    print(f"\n===== {show_title} =====")
    for src, dest in all_tasks:
        print(f"{src.name} -> {dest.name}")

def confirm():
    while True:
        confirm:str = input("\nProceed? [y/n] ").strip().lower()
        if confirm == "y":
            return True
        if confirm == "n":
            return False

def rename(src, dest):
    src.rename(dest)
    print(f"Success: {src.name} -> {dest.name}")

def main():
    args = parse_args()
    if args.recursive and args.dir:
        print("Error: --recursive + --dir not allowed")
        sys.exit(1)

    root = valid_dir(args.directory)
    items = list_items(root, args.recursive, args.dir)
    if not items:
        print("No items to rename")
        sys.exit(0)

    items:list[Path] = sort_items(items, args.sort)
    prefix = make_prefix(args)
    tasks = rename_plan(items, prefix)
    if not tasks:
        print("No items to rename")
        sys.exit(0)

    if args.preview:
        show(tasks, True)
        return

    if not args.yes:
        show(tasks, False)
        if not confirm():
            print("Cancelled")
            sys.exit(0)

    count = 0
    for src, dest in tasks:
        rename(src, dest)
        count += 1
    print(f"\nDone: {count}/{len(tasks)}")

if __name__ == "__main__":
    main()
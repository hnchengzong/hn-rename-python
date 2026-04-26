from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Tuple
from .args import SORT_TABLE

def list_items(root: Path, recursive: bool, dir_only: bool) -> List[Path]:
    items: List[Path] = []
    walker: Iterator[Path] = root.rglob("*") if recursive else root.iterdir()
    for item in walker:
        if item.name.startswith("."):
            continue
        if dir_only and item.is_dir():
            items.append(item)
        if not dir_only and item.is_file():
            items.append(item)
    return items

def sort_items(items: List[Path], mode: str) -> List[Path]:
    return SORT_TABLE[mode](items)

def make_prefix(args) -> str:
    parts: List[str] = []
    if args.time:
        parts.append(datetime.now().strftime("%Y%m%d"))
    if args.str and args.str.strip():
        parts.append(args.str.strip())
    return "_".join(parts) + "_" if parts else ""

def rename_plan(items: List[Path], prefix: str) -> List[Tuple[Path, Path]]:
    tasks: List[Tuple[Path, Path]] = []
    used = set()
    for idx, item in enumerate(items, 1):
        num: str = str(idx)
        suffix: str = item.suffix if item.is_file() else ""
        new_name: str = f"{prefix}{num}{suffix}"
        new_path: Path = item.parent / new_name
        if new_path.exists() or new_name in used:
            print(f"Skipped: {item.name} -> {new_name}")
            continue
        tasks.append((item, new_path))
        used.add(new_name)
    return tasks

def rename(src: Path, dest: Path):
    src.rename(dest)
    print(f"Success: {src.name} -> {dest.name}")
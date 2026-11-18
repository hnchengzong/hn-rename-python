import os
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
    sources = set(items)
    used = set()
    tasks: List[Tuple[Path, Path]] = []
    num = 1
    for item in items:
        suffix: str = item.suffix if item.is_file() else ""
        while True:
            new_path: Path = item.parent / f"{prefix}{num}{suffix}"
            if new_path in used:
                num += 1
                continue
            if new_path != item and os.path.lexists(new_path) and new_path not in sources:
                num += 1
                continue
            break
        used.add(new_path)
        num += 1
        if new_path != item:
            tasks.append((item, new_path))
    return tasks

def is_pure_permutation(items: List[Path], tasks: List[Tuple[Path, Path]]) -> bool:
    sources = set(items)
    return all(dest in sources for _, dest in tasks)

def _temp_path(src: Path) -> Path:
    idx = 0
    while True:
        tmp = src.parent / f".{src.name}.hn-rename-{os.getpid()}-{idx}.tmp"
        if not os.path.lexists(tmp):
            return tmp
        idx += 1

def rename_all(tasks: List[Tuple[Path, Path]]) -> int:
    pending = [(src, dest, src.name) for src, dest in tasks]
    done = 0
    while pending:
        progressed = False
        for task in list(pending):
            src, dest, label = task
            if os.path.lexists(dest):
                continue
            src.rename(dest)
            print(f"Success: {label} -> {dest.name}")
            pending.remove(task)
            done += 1
            progressed = True
        if progressed:
            continue
        src, dest, label = pending[0]
        busy = {t[0] for t in pending}
        if dest not in busy and os.path.lexists(dest):
            print(f"Conflict: {label} -> {dest.name} (target exists, skipped)")
            pending.remove(pending[0])
            continue
        tmp = _temp_path(src)
        src.rename(tmp)
        pending[0] = (tmp, dest, label)
    return done

from pathlib import Path
from typing import List, Tuple

def show(all_tasks: List[Tuple[Path, Path]], preview: bool):
    show_title = "Preview" if preview else "Pending"
    print(f"\n===== {show_title} =====")
    for src, dest in all_tasks:
        print(f"{src.name} -> {dest.name}")

def confirm() -> bool:
    while True:
        confirm: str = input("\nProceed? [y/n] ").strip().lower()
        if confirm in ("y", "yes"):
            return True
        if confirm in ("n", "no", ""):
            return False
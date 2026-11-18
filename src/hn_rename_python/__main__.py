#!/usr/bin/env python3
import sys
from .args import parse_args, valid_dir
from .file_ops import list_items, sort_items, make_prefix, rename_plan, rename_all, is_pure_permutation
from .ui import show, confirm

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

    items = sort_items(items, args.sort)
    prefix = make_prefix(args)
    tasks = rename_plan(items, prefix)
    if not tasks:
        print("Already numbered, nothing to do")
        sys.exit(0)

    if args.sort in ("name", "ctime") and is_pure_permutation(items, tasks):
        print(f"Already numbered, skipping --sort={args.sort} (it would only permute existing numbers)")
        sys.exit(0)

    if args.preview:
        show(tasks, True)
        return

    if not args.yes:
        show(tasks, False)
        if not confirm():
            print("Cancelled")
            sys.exit(0)

    count = rename_all(tasks)
    print(f"\nDone: {count}/{len(tasks)}")

if __name__ == "__main__":
    main()
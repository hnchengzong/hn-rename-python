#!/usr/bin/env python3
import sys
from .args import parse_args, valid_dir
from .file_ops import list_items, sort_items, make_prefix, rename_plan, rename
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
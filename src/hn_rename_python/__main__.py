import argparse
import sys
import datetime
import random
from pathlib import Path
from natsort import natsorted

def main():
    parser = argparse.ArgumentParser(description="A Python Batch Rename Tool")
    parser.add_argument("directory",nargs="?",default="." ,help="Choose directory(Default: current directory)")
    parser.add_argument("-p", "--preview", action="store_true", help="Preview files")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    parser.add_argument("-r","-R", "--recursive", action="store_true", help="Rename files in subdirectories")
    parser.add_argument("-t", "--time",action="store_true", help="Rename files with date")
    parser.add_argument("-s", "--str", default=None, help="Rename files with string(Need argument)")
    parser.add_argument("-d", "--dir", action="store_true", help="Rename directories")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s-python 0.1.3")
    parser.add_argument("--sort",default="natural",choices=["natural","name","size","mtime","ctime","owner","suffix","group","random"], help="Sort order:natural(default),name,size,mtime,ctime,owner,suffix,group,random")



    args = parser.parse_args()
    target_dir = Path(args.directory).expanduser().resolve()
    if not target_dir.exists():
        print(f"{target_dir} does not exist")
        return 1
    def get_directory_files(directory:Path, recursive:bool = False,dir:bool = False) -> list[Path]:
        match (recursive, dir):
            case (True, True):
                return [p for p in directory.rglob("*") if p.is_dir()]
            case (True, False):
                return [p for p in directory.rglob("*") if p.is_file()]
            case (False, True):
                return [p for p in directory.iterdir() if p.is_dir()]
            case (False, False):
                return [p for p in directory.iterdir() if p.is_file()]

    files = get_directory_files(target_dir, args.recursive,args.dir)
    if not files:
        print("No files found.")
        return 1
    match args.sort:
        case "natural":
            files = natsorted(files, key=lambda p: p.name)
        case "name":
            files.sort(key=lambda p: p.name)
        case "size":
            files.sort(key=lambda p: p.stat().st_size)
        case "mtime":
            files.sort(key=lambda p: p.stat().st_mtime)
        case "ctime":
            files.sort(key=lambda p: p.stat().st_ctime)
        case "owner":
            try:
                files.sort(key=lambda p: p.stat().st_uid)
            except (AttributeError, NotImplementedError, KeyError, OSError):
                print("Sorting by owner is not supported on this platform. Sorting by name instead.")
                files.sort(key=lambda p: p.name)
        case "suffix":
            files.sort(key=lambda p: p.suffix)
        case "group":
            try:
                files.sort(key=lambda p: p.stat().st_gid)
            except (AttributeError, NotImplementedError, KeyError, OSError):
                print("Sorting by group is not supported on this platform. Sorting by name instead.")
                files.sort(key=lambda p: p.name)
        case "random":
            random.shuffle(files)

    prefix_list = []
    if args.time:
        prefix_list.append(datetime.datetime.now().strftime("%Y%m%d"))
    if args.str is not None:
        prefix_list.append(args.str)
    prefix = "_".join(prefix_list) + "_" if prefix_list else ""
    file_rename = []
    for idx, old_path in enumerate(files):
        num = str(idx+1)
        if prefix:
            new_name = prefix + num + old_path.suffix
        else:
            new_name = num + old_path.suffix
        default_new_path = old_path.with_name(new_name)
        if default_new_path.exists():
            print(f"Skip {old_path.name} -> {new_name} (because target already exists)")
            continue
        file_rename.append((old_path, default_new_path))

    if not file_rename:
        print("No files to rename.")
        return

    if args.preview:
        for old_path, default_new_path in file_rename:
            print(f"{old_path.name} -> {default_new_path.name}")
        return
    if not args.yes:
        print("The following files will be renamed:")
        for old_path, default_new_path in file_rename:
            print(f"{old_path.name} -> {default_new_path.name}")

        confirm = input("Do you want to proceed? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return

    for old_path, default_new_path in file_rename:
        try:
                old_path.rename(default_new_path)
                print(f"Renamed {old_path.name} -> {default_new_path.name} successfully.")
        except OSError as e:
            try:
                    old_path.replace(default_new_path)
                    print(f"Renamed {old_path.name} -> {default_new_path.name} successfully (used replace due to cross-filesystem move).")
            except Exception as inner_exception:
                    print(f"Failed to rename {old_path.name} -> {default_new_path.name}: {inner_exception}")
        except Exception as exception:
                    print(f"Failed to rename {old_path.name} -> {default_new_path.name}: {exception}")



if __name__ == "__main__":
    sys.exit(main())
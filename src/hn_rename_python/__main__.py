import argparse
import sys

from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="A Python Bitch Rename Tool")

    parser.add_argument("directory",nargs="?",default="." ,help="Choose Directory(default: current directory)")
    parser.add_argument("-p", "--preview", action="store_true", help="Preview Files")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip Confirmation")


    args = parser.parse_args()
    target_dir = Path(args.directory).expanduser().resolve()

    if not target_dir.exists():
        print(f"{target_dir} does not exist")
        return 1
    def get_directory_files(directory:Path) -> list[Path]:
        return [p for p in directory.iterdir() if p.is_file()]

    files = get_directory_files(target_dir)
    if not files:
        print("No files found.")
        return
    
    file_rename = []
    for idx, old_path in enumerate(files):
        new_name = str(idx+1) + old_path.suffix
        new_path = old_path.with_name(new_name)
        if new_path.exists():
            print(f"Skip {old_path.name} -> {new_name} (because target already exists)")
            continue
        file_rename.append((old_path, new_path))
        
    if not file_rename:
        print("No files to rename.")
        return
    
    if args.preview:
        for old_path, new_path in file_rename:
            print(f"{old_path.name} -> {new_path.name}")
        return
    if not args.yes:
        print("The following files will be renamed:")
        for old_path, new_path in file_rename:
            print(f"{old_path.name} -> {new_path.name}")

        confirm = input("Do you want to proceed? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return
        if confirm == 'y':
            for old_path, new_path in file_rename:
                try:
                    old_path.rename(new_path)
                    print(f"Renamed {old_path.name} -> {new_path.name} successfully.")
                except Exception as exception:
                    print(f"Failed to rename {old_path.name} -> {new_path.name}: {exception}")



if __name__ == "__main__":
    sys.exit(main())

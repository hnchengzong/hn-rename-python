# hn-rename-python

[English](README_EN.md) | [中文](README.md)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-1E88E5?logo=python&logoColor=white)
![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?logo=archlinux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A minimal batch renaming tool written in Python for personal use.

## Features

- By default, only processes files in the specified directory (without recursing into subdirectories or hidden files).
- Uses natural sorting by default, renaming files sequentially as `1.original_extension`, `2.original_extension`, etc.
- Use `--sort` to sort by file size, owner, modification time, creation time, or randomly.
- `--sort=name` uses filename sorting instead of natural sorting (e.g., 10.txt comes before 2.txt).
- Use `-r` for recursive file search, `-t` to name with current date, and `-s` to name with a specified string.
- Use `-d` to rename directories.
- Use `uv run hn-rename -h` to view help.
- Only tested on Arch Linux.

## Installation

### Running from source (use uv)

1. Ensure you have `Python 3.10+` and `uv` installed
2. Clone the repository:

```bash

git clone --depth 1 https://github.com/hnchengzong/hn-rename-python.git
cd hn-rename-python
uv run hn-rename --args

```

### AUR

`paru -S hn-rename-python-bin`

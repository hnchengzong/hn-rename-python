# hn-rename-python

[English](README_EN.md) | [中文](README.md)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![uv](https://img.shields.io/badge/uv-1E88E5?logo=python&logoColor=white)
![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?logo=archlinux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

一个极简的使用python写的批量重命名工具,供我自己使用。

## 功能

- 默认仅处理指定目录下的文件（不递归子目录和隐藏文件）。
- 默认自然排序，依次默认重命名为 `1.原扩展名`、`2.原扩展名` ……
- 使用`--sort`来根据文件大小、所有者、修改时间，创建时间或随机进行排序。
- `--sort=name`会使用文件名排序而不是自然排序。比如10.txt会排在2.txt的前面。
- 使用`-r`来递归查找文件，`-t`以当前日期命名，`-s`以指定字符串命名。
- 使用`-d`来重命名目录。
- 使用 `uv run hn-rename -h`查看帮助。
- 只在Arch Linux上做过测试，不保证其他系统上的稳定性。

## 安装

### 从源码运行（推荐使用 uv）

1. 确保已安装`Python 3.10+`和`uv`
2. 克隆仓库：

```bash

   git clone --depth 1 https://github.com/hnchengzong/hn-rename-python.git
   cd hn-rename-python
   uv run hn-rename --args

```

### AUR

`paru -S hn-rename-python-bin`

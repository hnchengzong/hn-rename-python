# hn-rename-python

一个极简的使用python写的批量重命名工具,供我自己使用。

## 功能

- 目前仅处理指定目录下的直接文件（不递归子目录，不处理隐藏文件）
- 按文件名自然排序后，依次重命名为 `1.原扩展名`、`2.原扩展名` ……
- 使用 `uv run hn-rename -h`查看帮助
- 只在Arch Linux上做过测试，不保证其他系统的稳定性。


## 安装

### 从源码运行（推荐使用 uv）

1. 确保已安装`Python 3.14+`和`uv`
2. 克隆仓库：
   ```bash
   git clone https://github.com/hnchengzong/hn-rename-python.git
   cd hn-rename-python
   uv run hn-rename

### AUR
`paru -S hn_rename_python`
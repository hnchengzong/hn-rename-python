# hn-rename-python

一个极简的使用python写的批量重命名工具,供我自己使用。

## 功能

- 默认仅处理指定目录下的直接文件（不递归子目录和隐藏文件）。
- 默认按文件名排序，依次默认重命名为 `1.原扩展名`、`2.原扩展名` ……
- 使用`sort`来根据文件大小、所有者、修改时间，创建时间或随机进行排序。
- 使用`-r`来递归查找文件，`-d`以当前日期命名，`-s`以指定字符串命名,需单独使用。
- 使用 `uv run hn-rename -h`查看帮助。
- 只在Arch Linux上做过测试，不保证其他系统上的稳定性。


## 安装

### 从源码运行（推荐使用 uv）

1. 确保已安装`Python 3.14+`和`uv`
2. 克隆仓库：
   ```bash
   git clone https://github.com/hnchengzong/hn-rename-python.git
   cd hn-rename-python
   uv run hn-rename --args

### AUR
`paru -S hn-rename-python-bin`
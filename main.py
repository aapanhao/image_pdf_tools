"""
合并图片和pdf到一个pdf中
确认原始文件，排序顺序
1、将pdf转换为图片
2、将所有图片合并为一个pdf
"""

import sys

from images_to_pdfs import images_to_pdfs_tool
from merge_images_and_pdfs import merge_images_and_pdfs_tool


def main():
    print(f"请选择功能:\n1: 批量将图片转换为pdf;\n2: 将图片和pdf合并为一个pdf")
    tool_num = input("请选择 1或2: ")
    if tool_num == "1":
        images_to_pdfs_tool()
    elif tool_num == "2":
        merge_images_and_pdfs_tool()
    else:
        print(f"选择{tool_num}, 没有此功能选项")
        sys.exit()


if __name__ == '__main__':
    main()

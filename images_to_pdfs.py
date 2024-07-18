import os
import sys

from PIL import Image
from util import adjust_image_size

origin_file_dir = "tool_1_images"
target_file_dir = "tool_1_pdfs"


def images_to_pdfs_tool():
    init_dir()

    import_file_hint()

    confirm_image_files()

    images_to_pdfs()

    print(f"转换完成, 请到: {target_file_dir}文件夹下查看转换后的pdf文件")


def init_dir():
    if not os.path.exists(origin_file_dir):
        os.mkdir(origin_file_dir)

    if not os.path.exists(target_file_dir):
        os.mkdir(target_file_dir)


def import_file_hint():
    print(f"选择了: 批量将图片转换为pdf功能; 请将要转换的图片放在:{origin_file_dir} 文件夹下")
    is_completed = input("导入完成请按 Y: ")
    if is_completed.upper() != "Y":
        print(f"导入文件时退出")
        sys.exit()


def confirm_image_files():
    image_files = os.listdir(origin_file_dir)
    confirm = input(f"请确认是否将以下图片转换为pdf: {image_files} Y/N: ")
    if confirm.upper() != "Y":
        print("确认文件退出")
        sys.exit()

    if not image_files:
        print("没有找到图片文件")
        sys.exit()


def images_to_pdfs():
    image_width = input(f"可以设置图片宽度(常用选项: 1000或800), 如果不设置, 可以直接回车, 会以图片原始大小进行转换; width: ")
    print(f"图片宽度设置为: {image_width if image_width else '原始尺寸'}")
    print("开始转换图片为pdf...")
    image_files = os.listdir(origin_file_dir)
    for image_file in image_files:
        try:
            image_to_pdf(image_file, image_width)
        except Exception as e:
            print(f"{image_file} 转换失败, {str(e)}")


def image_to_pdf(image_file: str, image_width=None):
    image_file_path = os.path.join(origin_file_dir, image_file)
    image = Image.open(image_file_path).convert('RGB')
    adjust_image = adjust_image_size(image, image_width)

    image_file_name = image_file.split(".")[0]
    pdf_file_path = os.path.join(target_file_dir, f"{image_file_name}.pdf")

    adjust_image.save(pdf_file_path)
    print(f"{image_file} 转换成功 {pdf_file_path}")

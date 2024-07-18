import os
import sys

from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from util import adjust_image_size

origin_file_dir = "tool_2_images_and_pdfs"
target_file_dir = "tool_2_pdf"
tmp_file_dir = os.path.join(origin_file_dir, "tmp")


def merge_images_and_pdfs_tool():
    init_dir()

    import_file_hint()

    confirm_origin_files()

    merge_origin_files()

    print(f"合并完成, 请到: {target_file_dir} 文件夹下查看合并后的pdf文件")


def init_dir():
    if not os.path.exists(origin_file_dir):
        os.mkdir(origin_file_dir)

    if not os.path.exists(target_file_dir):
        os.mkdir(target_file_dir)

    if not os.path.exists(tmp_file_dir):
        os.mkdir(tmp_file_dir)


def import_file_hint():
    print(
        f"选择了: 批量将图片和pdf合并为一个pdf功能; 请将要转换的图片和pdf放在:{origin_file_dir} 文件夹下, 仅支持图片和pdf类型\n"
        f"如果有顺序要求, 请在文件名前加入前缀数字, 如: 1_文件名.jpg, 2_文件名.jpg, 3_文件名.pdf, 4_文件名.jpg...")
    is_completed = input("导入完成请按 Y: ")
    if is_completed.upper() != "Y":
        print(f"导入文件时退出")
        sys.exit()


def sort_key(s: str):
    x = s.split("_")[0]
    return int(x) if x.isdigit() else s


def sorted_origin_files():
    all_files = [f for f in os.listdir(origin_file_dir) if os.path.isfile(os.path.join(origin_file_dir, f))]
    origin_files = sorted(all_files, key=sort_key)
    return origin_files


def confirm_origin_files():
    origin_files = sorted_origin_files()
    origin_files_str = ", ".join(origin_files)
    confirm = input(f"请确认是否将以下文件，并「按此顺序」合并为pdf: {origin_files_str} Y/N: ")
    if confirm.upper() != "Y":
        print("确认文件退出")
        sys.exit()

    if not origin_files:
        print("没有找到要合并的文件")
        sys.exit()


def merge_origin_files():
    image_width = input(f"可以设置图片宽度(常用选项: 1000/800), 如果不设置, 可以直接回车, 会以图片原始大小进行转换; width: ")
    print(f"图片宽度设置为: {image_width if image_width else '原始尺寸'}")
    print("开始合并image和pdf为pdf...")

    pdf_writer = PdfWriter()

    origin_files = sorted_origin_files()
    for origin_file in origin_files:
        merge_file(pdf_writer, origin_file, image_width)

    save_pdf_writer(pdf_writer)


def merge_file(pdf_writer: PdfWriter, origin_file: str, image_width=None):
    origin_file_path = os.path.join(origin_file_dir, origin_file)
    try:
        if origin_file.endswith(".pdf"):
            merge_pdf(pdf_writer, origin_file_path)
        else:
            merge_image(pdf_writer, origin_file_path, image_width)
    except Exception as e:
        print(f"{origin_file_path} 合并失败, {str(e)}")


def merge_pdf(pdf_writer: PdfWriter, origin_file_path: str):
    pdf_reader = PdfReader(origin_file_path)
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)


def merge_image(pdf_writer: PdfWriter, origin_file_path: str, image_width=None):
    pdf_file_path = image_to_pdf(origin_file_path, image_width)
    merge_pdf(pdf_writer, pdf_file_path)


def image_to_pdf(origin_file_path, image_width=None) -> str:
    image = Image.open(origin_file_path).convert('RGB')
    adjust_image = adjust_image_size(image, image_width)

    image_file_name = origin_file_path.split("/")[-1].split(".")[0]
    pdf_file_path = os.path.join(tmp_file_dir, f"{image_file_name}.pdf")
    adjust_image.save(pdf_file_path)
    return pdf_file_path


def save_pdf_writer(pdf_writer: PdfWriter):
    output_pdf_path = os.path.join(target_file_dir, "output.pdf")
    with open(output_pdf_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

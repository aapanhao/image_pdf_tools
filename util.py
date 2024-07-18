from PIL import Image


def adjust_image_size(image: Image, image_width=None):
    if not image_width:
        return image

    image_width = int(image_width)
    if image.width > image_width:
        height = int((image_width / float(image.width)) * image.height)
        image = image.resize((image_width, height), Image.Resampling.LANCZOS)
    return image
